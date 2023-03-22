from pathlib import Path
from typing import Optional

from redcap.methods.reports import Reports

from datalad.interface.common_opts import (
    nosave_opt,
    save_message_opt,
)

from datalad_next.commands import (
    EnsureCommandParameterization,
    ValidatedInterface,
    Parameter,
    build_doc,
    datasetmethod,
    eval_results,
    get_status_dict,
)
from datalad_next.constraints import (
    EnsureBool,
    EnsurePath,
    EnsureStr,
    EnsureURL,
)
from datalad_next.constraints.dataset import (
    DatasetParameter,
    EnsureDataset,
)
from datalad_next.utils import CredentialManager

from .utils import (
    update_credentials,
    check_ok_to_edit,
)


@build_doc
class ExportReport(ValidatedInterface):
    """Export a report of the Project

    This is an equivalent to exporting a custom report via the "My
    Reports & Exports" page in REDCap's interface. A report must be
    defined through the REDCap's interface, and the user needs to look
    up its auto-generated report ID.
    """

    _params_ = dict(
        url=Parameter(
            args=("url",),
            doc="API URL to a REDCap server",
        ),
        report=Parameter(
            args=("report",),
            doc="""the report ID number, provided next to the report name
            on the report list page in REDCap UI.""",
            metavar="report_id",
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
            report=EnsureStr(),
            outfile=EnsurePath(),
            dataset=EnsureDataset(installed=True, purpose="export REDCap report"),
            credential=EnsureStr(),
            message=EnsureStr(),
            save=EnsureBool(),
        ),
        validate_defaults=("dataset",),
        tailor_for_dataset=({"outfile": "dataset"}),
    )

    @staticmethod
    @datasetmethod(name="export_redcap_report")
    @eval_results
    def __call__(
        url: str,
        report: str,
        outfile: Path,
        dataset: Optional[DatasetParameter] = None,
        credential: Optional[str] = None,
        message: Optional[str] = None,
        save: bool = True,
    ):

        ds = dataset.ds

        # refuse to operate if target file is outside the dataset or not clean
        ok_to_edit, unlock = check_ok_to_edit(outfile, ds)
        if not ok_to_edit:
            yield get_status_dict(
                action="export_redcap_report",
                path=outfile,
                status="error",
                message=(
                    "Output file status is not clean or the file does not "
                    "belong directly to the reference dataset."
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
        api = Reports(
            url=url,
            token=credprops["secret"],
        )

        # perform the api query
        response = api.export_report(
            report_id=report,
            format_type="csv",
        )

        # query went well, store or update credentials
        update_credentials(credman, credname, credprops)

        # unlock the file if needed, and write contents
        if unlock:
            ds.unlock(outfile)
        with open(outfile, "wt") as f:
            f.write(response)

        # save changes in the dataset
        if save:
            ds.save(
                message=message if message is not None else "Export REDCap report",
                path=outfile,
            )

        # yield successful result if we made it to here
        yield get_status_dict(
            action="export_redcap_report",
            path=outfile,
            status="ok",
        )
