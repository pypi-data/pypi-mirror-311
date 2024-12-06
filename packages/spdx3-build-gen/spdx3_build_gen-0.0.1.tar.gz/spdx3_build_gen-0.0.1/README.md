# spdx3-build-gen
A command line tool for generating SPDX 3 build SBoMs from lists of input and
output files

## Installation

`spdx3-build-gen` can be installed using `pip`:

```shell
python3 -m pip install spdx3-build-gen
```

## Usage

## Development

Development on `spdx3-build-gen` can be done by setting up a virtual
environment and installing it in editable mode:

```shell
python3 -m venv .venv
. .venv/bin/activate
pip install -e .[dev]
```

Tests can be run using pytest:

```shell
pytest -v
```
