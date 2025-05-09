"""Export one or multiple forms"""

import logging
from pathlib import Path
import textwrap
from typing import (
    List,
    Optional,
)

from redcap.methods.records import Records

from datalad.interface.common_opts import (
    nosave_opt,
    save_message_opt,
)
from datalad_next.commands import (
    EnsureCommandParameterization,
    Parameter,
    ValidatedInterface,
    build_doc,
    datasetmethod,
    eval_results,
    get_status_dict,
)
from datalad_next.constraints import (
    EnsureBool,
    EnsureListOf,
    EnsurePath,
    EnsureStr,
    EnsureURL,
    DatasetParameter,
)
from datalad_next.constraints.dataset import (
    EnsureDataset,
)
from datalad_next.utils import CredentialManager

from .utils import (
    update_credentials,
    check_ok_to_edit,
)

__docformat__ = "restructuredtext"
lgr = logging.getLogger("datalad.redcap.export_form")


@build_doc
class ExportForm(ValidatedInterface):
    """Export records from selected forms (instruments)

    This is an equivalent to "Selected Instruments" export option in
    REDCap's interface.  Allows saving response data from one or
    several forms into a single csv file.
    """

    _params_ = dict(
        url=Parameter(
            args=("url",),
            doc="API URL to a REDCap server",
        ),
        forms=Parameter(
            args=("forms",),
            doc="project form name(s)",
            nargs="+",
            metavar="form",
        ),
        outfile=Parameter(
            args=("outfile",),
            doc="file to write. Existing files will be overwritten.",
        ),
        dataset=Parameter(
            args=("-d", "--dataset"),
            metavar="PATH",
            doc="""the dataset in which the output file will be saved.
            The `outfile` argument will be interpreted as being relative to
            this dataset.  If no dataset is given, it will be identified
            based on the working directory.""",
        ),
        survey_fields=Parameter(
            args=("--no-survey-fields",),
            dest="survey_fields",
            action="store_false",
            doc="do not include survey identifier or survey timestamp fields",
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
        message=save_message_opt,
        save=nosave_opt,
    )

    _validator_ = EnsureCommandParameterization(
        dict(
            url=EnsureURL(required=["scheme", "netloc", "path"]),
            forms=EnsureListOf(str),
            outfile=EnsurePath(),
            dataset=EnsureDataset(installed=True, purpose="export REDCap form"),
            survey_fields=EnsureBool(),
            credential=EnsureStr(),
            message=EnsureStr(),
            save=EnsureBool(),
        ),
        validate_defaults=("dataset",),
        tailor_for_dataset=({"outfile": "dataset"}),
    )

    @staticmethod
    @datasetmethod(name="export_redcap_form")
    @eval_results
    def __call__(
        url: str,
        forms: List[str],
        outfile: Path,
        dataset: Optional[DatasetParameter] = None,
        survey_fields: bool = True,
        credential: Optional[str] = None,
        message: Optional[str] = None,
        save: bool = True,
    ):

        ds = dataset.ds

        # refuse to operate if target file is outside the dataset or not clean
        ok_to_edit, unlock = check_ok_to_edit(outfile, ds)
        if not ok_to_edit:
            yield get_status_dict(
                action="export_redcap_form",
                path=outfile,
                status="error",
                message=(
                    "Output file status is not clean or it is not directly "
                    "under the reference dataset."
                ),
            )
            return

        # determine a token
        credman = CredentialManager(ds.config)
        credname, credprops = credman.obtain(
            name=credential,
            prompt="A token is required to access the REDCap project API",
            type_hint="token",
            query_props={"realm": url},
            expected_props=("secret",),
        )

        # create an api object
        api = Records(
            url=url,
            token=credprops["secret"],
        )

        # perform the api query
        # for csv format, outputs result as string
        # raises RedcapError if token or form name are incorrect
        response = api.export_records(
            format_type="csv",
            forms=forms,
            export_survey_fields=survey_fields,
        )

        # query went well, store or update credentials
        update_credentials(credman, credname, credprops)

        # unlock the file if needed, and write contents
        if unlock:
            yield from ds.unlock(
                outfile, result_renderer="disabled", return_type="generator"
            )
        with open(outfile, "wt") as f:
            f.write(response)

        # save changes in the dataset
        if save:
            ds.save(
                message=message
                if message is not None
                else _write_commit_message(forms),
                path=outfile,
            )

        # yield successful result if we made it to here
        yield get_status_dict(
            action="export_redcap_form",
            path=outfile,
            status="ok",
        )


def _write_commit_message(which_forms: List[str]) -> str:
    """Return a formatted commit message that includes form names"""
    forms = ", ".join(which_forms)
    header = "Export REDCap forms"
    body = "\n".join(textwrap.wrap(f"Contains the following forms: {forms}."))
    return header + "\n\n" + body
