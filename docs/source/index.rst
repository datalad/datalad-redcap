DataLad REDCap extension
************************

This DataLad extension provides convenience commands for exporting
data from REDCap into DataLad datasets. Information about the RedCAP
project can be found at https://project-redcap.org/.

Installation
============

The extension is a working prototype. It can be installed from
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

Acknowledgements
================

This DataLad extension was developed with funding from the Deutsche
Forschungsgemeinschaft (DFG, German Research Foundation) under grant
SFB 1451 (`431549029 <https://gepris.dfg.de/gepris/projekt/431549029>`_,
INF project).

.. |---| unicode:: U+02014 .. em dash
