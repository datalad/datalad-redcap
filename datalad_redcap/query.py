"""Query REDCap's API for exportable items"""

import os
from typing import Optional

from prettytable import PrettyTable
from redcap.methods.instruments import Instruments

from datalad.interface.base import (
    Interface,
    build_doc,
)
from datalad.interface.results import get_status_dict
from datalad.interface.utils import eval_results
from datalad.support.constraints import (
    EnsureStr,
    EnsureChoice,
)
from datalad.support.param import Parameter
from datalad.ui import ui
from datalad_next.utils import CredentialManager

from .utils import update_credentials


class MyInstruments(Instruments):
    """An extension of PyCap's Instruments class

    Contains an additional method to export instruments names and labels
    """

    def export_instruments(self):
        """Export instruments names and labels

        PyCap's Instruments class has a field_names property, but lacks
        a method to return matching labels (human-readable). This method
        does that in a simplified way (only supports json format, does not
        support arms).
        """
        format_type = "json"  # constant, for now
        payload = self._initialize_payload(
            content="instrument",
            format_type=format_type,
        )
        return_type = self._lookup_return_type(format_type, request_type="export")
        response = self._call_api(payload, return_type)

        return self._return_data(
            response=response,
            content="instrument",
            format_type=format_type,
            df_kwargs=None,
        )


@build_doc
class Query(Interface):
    """Query REDCap's API for available instruments (data entry forms)

    Can be used to retrieve human-oriented labels and API-oriented names of
    instruments (data entry forms) which can be exported from the project.
    [PY: Returns a result record dictionary res in which "instruments" key
    contains a list where each instrument is represented as a dictionary with
    "instrument name" and "instrument_label" keys.][CMD: Displays a table with
    results].
    """

    result_renderer = "tailored"

    _params_ = dict(
        url=Parameter(
            args=("url",),
            doc="API URL to a REDCap server",
            constraints=EnsureStr(),
        ),
        credential=Parameter(
            args=("--credential",),
            metavar="name",
            doc="""name of the credential providing a token to be used for
            authorization. If a match for the name is found, it will
            be used; otherwise the user will be prompted and the
            credential will be saved. If the name is not provided, the
            last-used credential matching the API url will be used if
            present; otherwise the user will be prompted and the
            credential will be saved under a default name.""",
        ),
    )

    @staticmethod
    @eval_results
    def __call__(url: str, credential: Optional[str] = None):

        # determine the token
        credman = CredentialManager()
        credname, credprops = credman.obtain(
            name=credential,
            prompt="A token is required to access the REDCap project API",
            type_hint="token",
            query_props={"realm": url},
            expected_props=("secret",),
        )

        # perform api query
        api = MyInstruments(url=url, token=credprops["secret"])
        instruments = api.export_instruments()

        # query went well, store or update credentials
        update_credentials(credman, credname, credprops)

        yield get_status_dict(
            action="redcap_query",
            path=os.getcwd(),
            status="ok",
            instruments=instruments,
        )

    @staticmethod
    def custom_result_renderer(res, **_):
        """A custom results renderer which prints a formatted table"""

        if res["status"] != "ok" or res.get("action", "") != "redcap_query":
            return

        tbl = PrettyTable()
        tbl.field_names = ["Instrument label", "Instrument name"]
        tbl.align = "l"
        for x in res.get("instruments", []):
            tbl.add_row([x["instrument_label"], x["instrument_name"]])
        ui.message(tbl.get_string())
