#! /bin/sh

SPDX_VERSION="3.0.1"

exec shacl2code generate \
    -i https://spdx.org/rdf/$SPDX_VERSION/spdx-model.ttl \
    -i https://spdx.org/rdf/$SPDX_VERSION/spdx-json-serialize-annotations.ttl \
    -x https://spdx.org/rdf/$SPDX_VERSION/spdx-context.jsonld python \
    -o spdx3.py
