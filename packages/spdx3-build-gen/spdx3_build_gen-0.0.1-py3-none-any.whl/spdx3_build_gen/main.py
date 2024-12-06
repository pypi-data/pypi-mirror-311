#! /usr/bin/env python3
#
# Copyright (c) 2024 Joshua Watt
#
# SPDX-License-Identifier: MIT


import argparse
import sys
import uuid
import hashlib
import re
import os
from datetime import datetime, timezone
from pathlib import Path


from . import spdx3
from .version import VERSION


LIC_REGEX = re.compile(
    rb"^\W*SPDX-License-Identifier:\s*([ \w\d.()+-]+?)(?:\s+\W*)?$",
    re.MULTILINE,
)


def parse_file_lists(file_lists):
    result = []
    for lst, base in file_lists:
        with lst.open("r") as f:
            result.extend([(line.rstrip(), base) for line in f.readlines()])

    result.sort()
    return result


def main():
    parser = argparse.ArgumentParser(description="Create build SBoM from source list")

    parser.add_argument("--version", "-V", action="version", version=VERSION)
    parser.add_argument(
        "--sources",
        "-s",
        nargs=2,
        metavar="SOURCES SRCDIR",
        type=Path,
        help="Path to list of source files and base source directory",
        action="append",
        default=[],
    )
    parser.add_argument(
        "--builds",
        "-b",
        nargs=2,
        metavar="BUILDS BUILDDIR",
        type=Path,
        help="Path to list of build files and base build directory",
        action="append",
        default=[],
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("output.spdx.json"),
        help="path to SPDX output file. Default is '%(default)s'",
    )
    parser.add_argument(
        "-n",
        "--namespace-prefix",
        help="Prefix for SPDX document namespaces. If unspecified a random namespace will be used",
        default=f"http://spdx.org/spdxdocs/{str(uuid.uuid4())}",
    )
    parser.add_argument(
        "--package-name",
        help="Package name",
    )
    parser.add_argument(
        "--package-version",
        help="Package version",
    )
    parser.add_argument(
        "--package-license",
        help="Declared license for package",
    )
    parser.add_argument(
        "-p",
        "--pretty",
        help="Pretty print JSON output",
        action="store_true",
    )
    parser.add_argument(
        "--author-person",
        help="Document author (person)",
        action="append",
        default=[],
    )
    parser.add_argument(
        "--author-org",
        help="Document author (organization)",
        action="append",
        default=[],
    )
    parser.add_argument(
        "--author-spdxid",
        help="Document author (external SpdxId)",
        action="append",
        default=[],
    )
    parser.add_argument(
        "--build-type",
        metavar="IRI",
        help="The IRI that identifies what type of build was done",
        required=True,
    )
    parser.add_argument(
        "--build-time",
        metavar="DATETIME",
        help="Build time in ISO 8601 format. If omitted, the current time is used",
        type=datetime.fromisoformat,
        default=datetime.now(),
    )
    parser.add_argument(
        "--import",
        metavar="SPDXID URL",
        nargs=2,
        dest="imports",
        help="Import SPDXID from external SPDX document at URL",
        action="append",
        default=[],
    )

    def add_agent_group(name, desc):
        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            f"--{name}-person",
            metavar="NAME",
            help=f"{desc} (person)",
        )
        group.add_argument(
            f"--{name}-org",
            metavar="NAME",
            help=f"{desc} (organization)",
        )
        group.add_argument(
            f"--{name}-tool",
            metavar="NAME",
            help=f"{desc} (tool)",
        )
        group.add_argument(
            f"--{name}-spdxid",
            metavar="SPDXID",
            help=f"{desc} (external SpdxId)",
        )

    add_agent_group("build-invoked-by", "Agent invoking the build")
    add_agent_group("build-on-behalf-of", "Agent on who's behalf the build was invoked")
    add_agent_group("supplier", "Package Supplier")

    parser.add_argument(
        "--hash",
        metavar="ALGORITHM",
        help="Hash algorithms to use for files. If unspecified, defaults to 'sha256'",
        choices=hashlib.algorithms_available,
        action="append",
        default=[],
    )

    args = parser.parse_args()

    objset = spdx3.SHACLObjectSet()

    creation_info = spdx3.CreationInfo(
        created=datetime.now(tz=timezone.utc),
        specVersion="3.0.1",
    )

    def make_id(suffix):
        spdxid = f"{args.namespace_prefix.rstrip('/')}/{suffix}"
        return re.sub(r"[^A-Za-z0-9:/_.-]", "_", spdxid)

    def make_agent(name, cls):
        for c in creation_info.createdBy:
            if isinstance(c, cls) and c.name == name:
                return c

        return cls(
            _id=make_id(f"{cls.__name__}/{name}"),
            name=name,
            creationInfo=creation_info,
        )

    def get_args_agent(name):
        if v := getattr(args, f"{name}_person"):
            return objset.add(make_agent(v, spdx3.Person))

        if v := getattr(args, f"{name}_org"):
            return objset.add(make_agent(v, spdx3.Organization))

        if v := getattr(args, f"{name}_tool"):
            return objset.add(make_agent(v, spdx3.Tool))

        if v := getattr(args, f"{name}_spdxid"):
            return v

    idx = 0

    def inc_index():
        nonlocal idx
        idx += 1
        return idx

    def create_hashes(path):
        if not args.hash:
            hashes = [hashlib.sha256()]
        else:
            hashes = [hashlib.new(n) for n in args.hash]

        with path.open("rb") as f:
            while True:
                b = f.read(4096)
                if not b:
                    break

                for h in hashes:
                    h.update(b)

        return [
            spdx3.Hash(
                algorithm=getattr(spdx3.HashAlgorithm, h.name),
                hashValue=h.hexdigest(),
            )
            for h in hashes
        ]

    def make_license(lic):
        for o in objset.foreach_type(spdx3.simplelicensing_LicenseExpression):
            if o.simplelicensing_licenseExpression == lic:
                return o

        return spdx3.simplelicensing_LicenseExpression(
            _id=make_id(f"License/{inc_index()}"),
            simplelicensing_licenseExpression=lic,
            creationInfo=creation_info,
        )

    def extract_licenses(path):
        """
        Extract SPDX License identifiers from a file
        """
        ascii_licenses = []
        try:
            with path.open("rb") as f:
                size = min(15000, os.stat(path).st_size)
                txt = f.read(size)
                licenses = re.findall(LIC_REGEX, txt)
                if licenses:
                    for lic in licenses:
                        try:
                            ascii_licenses.append(lic.decode("ascii"))
                        except UnicodeDecodeError:
                            pass
        except OSError:
            pass

        lic_objs = [objset.add(make_license(lic)) for lic in ascii_licenses]
        if not lic_objs:
            lic_objs.append(spdx3.Element.NoneElement)

        return lic_objs

    def make_file(fn, base):
        file = objset.add(
            spdx3.software_File(
                _id=make_id(f"File/{inc_index()}"),
                creationInfo=creation_info,
                name=str(fn),
                verifiedUsing=create_hashes(base / fn),
                software_fileKind=spdx3.software_FileKindType.file,
                software_primaryPurpose=spdx3.software_SoftwarePurpose.source,
            )
        )
        objset.add(
            spdx3.Relationship(
                _id=make_id(f"Relationship/{inc_index()}"),
                relationshipType=spdx3.RelationshipType.hasConcludedLicense,
                creationInfo=creation_info,
                from_=file,
                to=extract_licenses(base / fn),
            )
        )
        return file

    for a in args.author_person:
        person = objset.add(make_agent(a, spdx3.Person))
        creation_info.createdBy.append(person)

    for a in args.author_org:
        org = objset.add(make_agent(a, spdx3.Organization))
        creation_info.createdBy.append(org)

    for a in args.author_spdxid:
        creation_info.createdBy.append(a)

    if not creation_info.createdBy:
        print("ERROR: At least one author must be specified")
        return 1

    # Add tool
    tool_name = os.path.basename(sys.argv[0])
    creation_info.createdUsing.append(
        objset.add(
            spdx3.Tool(
                _id=make_id(f"Tool/{tool_name}"),
                name=f"{tool_name} version {VERSION}",
                creationInfo=creation_info,
            )
        )
    )

    # Add output package
    pkg = objset.add(
        spdx3.software_Package(
            _id=make_id("Package"),
            creationInfo=creation_info,
        )
    )

    if args.package_name:
        pkg.name = args.package_name

    if args.package_version:
        pkg.software_packageVersion = args.package_version

    if args.package_license:
        objset.add(
            spdx3.Relationship(
                _id=make_id(f"Relationship/{inc_index()}"),
                relationshipType=spdx3.RelationshipType.hasDeclaredLicense,
                creationInfo=creation_info,
                from_=pkg,
                to=[make_license(args.package_license)],
            )
        )

    if o := get_args_agent("supplier"):
        pkg.suppliedBy = o

    # Create build
    build = objset.add(
        spdx3.build_Build(
            _id=make_id("Build"),
            creationInfo=creation_info,
            build_buildType=args.build_type,
        )
    )
    if o := get_args_agent("build_invoked_by"):
        r = objset.add(
            spdx3.LifecycleScopedRelationship(
                _id=make_id(f"Relationship/{inc_index()}"),
                relationshipType=spdx3.RelationshipType.invokedBy,
                creationInfo=creation_info,
                scope=spdx3.LifecycleScopeType.build,
                from_=build,
                to=[o],
            )
        )

        if o := get_args_agent("build_on_behalf_of"):
            objset.add(
                spdx3.LifecycleScopedRelationship(
                    _id=make_id(f"Relationship/{inc_index()}"),
                    relationshipType=spdx3.RelationshipType.onBehalfOf,
                    creationInfo=creation_info,
                    scope=spdx3.LifecycleScopeType.build,
                    from_=r,
                    to=[o],
                )
            )

    # Create source files
    src_files = [make_file(fn, base) for fn, base in parse_file_lists(args.sources)]
    if src_files:
        objset.add(
            spdx3.LifecycleScopedRelationship(
                _id=make_id(f"Relationship/{inc_index()}"),
                relationshipType=spdx3.RelationshipType.hasInput,
                creationInfo=creation_info,
                scope=spdx3.LifecycleScopeType.build,
                from_=build,
                to=src_files,
            )
        )

    # Create build files
    build_files = [make_file(fn, base) for fn, base in parse_file_lists(args.builds)]
    if build_files:
        for f in build_files:
            f.builtTime = (args.build_time or datetime.now()).astimezone(timezone.utc)

        objset.add(
            spdx3.LifecycleScopedRelationship(
                _id=make_id(f"Relationship/{inc_index()}"),
                relationshipType=spdx3.RelationshipType.hasOutput,
                creationInfo=creation_info,
                scope=spdx3.LifecycleScopeType.build,
                from_=build,
                to=build_files,
            )
        )

    objset.add(
        spdx3.Relationship(
            _id=make_id(f"Relationship/{inc_index()}"),
            relationshipType=spdx3.RelationshipType.contains,
            creationInfo=creation_info,
            from_=pkg,
            to=build_files or [spdx3.Element.NoneElement],
        )
    )

    # Add all Elements currently in the object set to the SBoM
    sbom = objset.add(
        spdx3.software_Sbom(
            _id=make_id("SBOM"),
            creationInfo=creation_info,
            software_sbomType=[spdx3.software_SbomType.build],
            profileConformance=[
                spdx3.ProfileIdentifierType.core,
                spdx3.ProfileIdentifierType.build,
                spdx3.ProfileIdentifierType.simpleLicensing,
                spdx3.ProfileIdentifierType.software,
            ],
            rootElement=[build],
            element=sorted(objset.foreach_type(spdx3.Element, match_subclass=True)),
        )
    )

    # Create the SPDX Document
    doc = objset.add(
        spdx3.SpdxDocument(
            _id=make_id("Document"),
            creationInfo=creation_info,
            rootElement=[sbom],
        )
    )
    for spdxid, url in args.imports:
        doc.import_.append(
            spdx3.ExternalMap(
                externalSpdxId=spdxid,
                locationHint=url,
            )
        )

    # Write out document
    with args.output.open("wb") as f:
        spdx3.JSONLDSerializer().write(objset, f, indent=2 if args.pretty else None)

    return 0
