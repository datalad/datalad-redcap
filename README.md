# DataLad REDCap extension

[![crippled-filesystems](https://github.com/datalad/datalad-redcap/workflows/crippled-filesystems/badge.svg)](https://github.com/datalad/datalad-redcap/actions/workflows/test_crippledfs.yml)
[![docs](https://github.com/datalad/datalad-redcap/workflows/docs/badge.svg)](https://github.com/datalad/datalad-redcap/actions/workflows/docbuild.yml)

This DataLad extension provides convenience commands for exporting data from REDCap into DataLad datasets.
Information about the RedCAP project can be found at https://project-redcap.org/.

The extension is in early development.

## Commands
- `export-redcap-form`: Export records from selected forms (instruments)

## Usage examples
Credential management is not yet supported, and the API token will be read from the environment variable.
The example below will export a given form from REDCap in csv format and save the file in a DataLad dataset.
```
export REDCAP_TOKEN=<token>
datalad create my-exports
cd my-exports
datalad export-redcap-form <api url> <form label> exported.csv
```
