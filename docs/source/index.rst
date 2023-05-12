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

Index
=====

.. toctree::
   :maxdepth: 1

   command_line_reference
   python_module_reference
   user_guide
   design_docs

.. |---| unicode:: U+02014 .. em dash
