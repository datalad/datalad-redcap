Design docs
===========

Overview
--------

The extension should provide means for exporting data from REDCap into
DataLad datasets. Two primary use cases are: retrieving (updating)
selected data items while a study is ongoing, and archiving all
project data once a project is completed.

Generally, a command provided by this extension needs to combine an
API query with a DataLad ``save`` command, and produce a text file
tracked in a dataset. The extension should support the most relevant
options corresponding to the "Data Export, Reports and Stats" section
of REDCap's UI.

PyCap
-----

This extension uses `PyCap <https://redcap-tools.github.io/PyCap/>`_
library to interact with REDCap API. PyCap provides classes
responsible for the API methods.

Although queries could be executed just with the built-in requests
library (REDCap provides an API playground which can help generate
request-based queries), PyCap provides useful assertions (e.g for
token length), error handling with meaningful messages (e.g. raising
`RedcapError` for incorrect query or denied access), and convenience
enhancements (adding ID column to form exports).

Code style
----------

None of this is a strict requirement, but it is recommended to:

* use `black <https://black.readthedocs.io/en/stable/index.html>`_
  code style
* use `typing hints <https://peps.python.org/pep-0484/>`_
