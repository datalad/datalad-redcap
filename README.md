# DataLad REDCap extension

[![Documentation Status](https://readthedocs.org/projects/datalad-redcap/badge/?version=latest)](http://docs.datalad.org/projects/redcap/en/latest/?badge=latest)

[![crippled-filesystems](https://github.com/datalad/datalad-redcap/workflows/crippled-filesystems/badge.svg)](https://github.com/datalad/datalad-redcap/actions/workflows/test_crippledfs.yml)
[![docs](https://github.com/datalad/datalad-redcap/workflows/docs/badge.svg)](https://github.com/datalad/datalad-redcap/actions/workflows/docbuild.yml)

This DataLad extension provides convenience commands for exporting data from REDCap into DataLad datasets.
Information about the RedCAP project can be found at https://project-redcap.org/.

The extension is a working prototype.

## Installation
The extension has no official release yet, but you can install the *bleeding edge* version using pip, directly from GitHub.
This will also install the latest development version of [DataLad Next](https://github.com/datalad/datalad-next) extension.
Using a virtual environment is recommended.
Example installation:

```
# create and enter a new virtual environment (optional)
$ virtualenv --python=python3 ~/env/dl-redcap
$ source ~/env/dl-redcap/bin/activate
# install from GitHub main branch
$ python -m pip install git+https://github.com/datalad/datalad-redcap.git@main
```

## Commands
- `export-redcap-form`: Export records from selected forms (instruments)
- `export-redcap-project-xml`: Export entire project as a REDCap XML File
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

## Acknowledgements

This DataLad extension was developed with support from the Deutsche
Forschungsgemeinschaft (DFG, German Research Foundation) under grant SFB 1451
([431549029](https://gepris.dfg.de/gepris/projekt/431549029), INF project).
