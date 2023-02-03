"""DataLad demo extension"""

__docformat__ = 'restructuredtext'

import logging
lgr = logging.getLogger('datalad.redcap')

# Defines a datalad command suite.
# This variable must be bound as a setuptools entrypoint
# to be found by datalad
command_suite = (
    # description of the command suite, displayed in cmdline help
    "DataLad-Redcap command suite",
    [
        # specification of a command, any number of commands can be defined
        (
            # importable module that contains the command implementation
            'datalad_redcap.export_form',
            # name of the command class implementation in above module
            'ExportForm',
            # optional name of the command in the cmdline API
            'export-redcap-form',
            # optional name of the command in the Python API
            'export_redcap_form'
        ),
        (
            'datalad_redcap.export_report',
            'ExportReport',
            'export-redcap-report',
            'export_redcap_report'
        ),
        (
            'datalad_redcap.query',
            'Query',
            'redcap-query',
            'redcap_query'
        )
    ]
)

from . import _version
__version__ = _version.get_versions()['version']
