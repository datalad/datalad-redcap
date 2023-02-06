# DataLad REDCap extension

[![crippled-filesystems](https://github.com/datalad/datalad-redcap/workflows/crippled-filesystems/badge.svg)](https://github.com/datalad/datalad-redcap/actions/workflows/test_crippledfs.yml)
[![docs](https://github.com/datalad/datalad-redcap/workflows/docs/badge.svg)](https://github.com/datalad/datalad-redcap/actions/workflows/docbuild.yml)
[![Documentation Status](https://readthedocs.org/projects/datalad-redcap/badge/?version=latest)](http://docs.datalad.org/projects/redcap/en/latest/?badge=latest)

This DataLad extension provides convenience commands for exporting data from REDCap into DataLad datasets.
Information about the RedCAP project can be found at https://project-redcap.org/.

The extension is in early development.

## Commands
- `export-redcap-form`: Export records from selected forms (instruments)
- `export-redcap-report`: Export a report that was defined in a project
- `redcap-query`: Show names of available forms (instruments)

## Usage examples
The example below will show available forms, export a given form from REDCap in csv format, and save the file in a DataLad dataset.
```
datalad create my-exports
cd my-exports
datalad redcap-query <api url>
datalad export-redcap-form <api url> <form name> exported.csv
```
