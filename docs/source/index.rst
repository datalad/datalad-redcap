DataLad REDCap extension
************************

This DataLad extension provides convenience commands for exporting
data from REDCap into DataLad datasets. Information about the RedCAP
project can be found at https://project-redcap.org/.

Installation
============

The extension is in early development. It can be installed from
GitHub::

  # create and enter a new virtual environment (optional)
  $ virtualenv --python=python3 ~/env/dl-redcap
  $ source ~/env/dl-redcap/bin/activate
  # install from GitHub main branch
  $ python -m pip install git+https://github.com/datalad/datalad-redcap.git@main


API
===

High-level API commands
-----------------------

.. currentmodule:: datalad.api
.. autosummary::
   :toctree: generated

   export_redcap_form
   export_redcap_project_xml
   export_redcap_report
   redcap_query


Command line reference
----------------------

.. toctree::
   :maxdepth: 1

   generated/man/datalad-export-redcap-form
   generated/man/datalad-export-redcap-project-xml
   generated/man/datalad-export-redcap-report
   generated/man/datalad-redcap-query.rst


User guide
==========

.. toctree::
   :maxdepth: 1

   user_guide

Design
======

.. toctree::
   :maxdepth: 1

   design_docs


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. |---| unicode:: U+02014 .. em dash
