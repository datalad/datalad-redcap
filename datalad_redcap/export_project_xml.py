from pathlib import Path
from typing import Optional

from redcap.methods.project_info import ProjectInfo

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


def export_project_xml(
    self,
    metadata_only: bool = False,
    files: bool = False,
    survey_fields: bool = False,
    dags: bool = False,
):
    """Export Project XML

    This function is a patch for PyCap ProjectInfo class
    """

    format_type = "xml"
    payload = self._initialize_payload(
        content="project_xml",
        format_type=format_type,
    )

    payload["returnMetadataOnly"] = metadata_only
    payload["exportFiles"] = files
    payload["exportSurveyFields"] = survey_fields
    payload["exportDataAccessGroups"] = dags

    return_type = self._lookup_return_type(format_type, request_type="export")
    response = self._call_api(payload, return_type)

    return self._return_data(
        response=response,
        content="instrument",
        format_type=format_type,
        df_kwargs=None,
    )


# monkey-patch ProjectInfo
ProjectInfo.export_project_xml = export_project_xml


@build_doc
class ExportProjectXML(ValidatedInterface):
    """Export entire project (metadata & data) as a REDCap XML file

    This exports all the project content (all records, events, arms,
    instruments, fields, and project attributes) as a single XML
    file. The file can be used to create a clone of the project on the
    same or another REDCap instance. It can also be useful for
    archival.

    By default, the export will include all data as well. You can
    choose to export metadata only.

    Note that when exporting data, Data Export user rights will be
    applied to any returned data. 'Full Data Set' export rights in the
    project are required to obtain everything.
    """

    _params_ = dict(
        url=Parameter(
            args=("url",),
            doc="API URL to a REDCap server",
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
        metadata_only=Parameter(
            args=("--metadata-only",),
            action="store_true",
            doc="""return only metadata (all fields, forms, events, and arms),
            do not include data.""",
        ),
        survey_fields=Parameter(
            args=("--no-survey-fields",),
            dest="survey_fields",
            action="store_false",
            doc="do not include survey identifier or survey timestamp fields.",
        ),
        message=save_message_opt,
        save=nosave_opt,
    )

    _validator_ = EnsureCommandParameterization(
        dict(
            url=EnsureURL(required=["scheme", "netloc", "path"]),
            outfile=EnsurePath(),
            dataset=EnsureDataset(installed=True, purpose="export REDCap project XML"),
            credential=EnsureStr(),
            metadata_only=EnsureBool(),
            survey_fields=EnsureBool(),
            message=EnsureStr(),
            save=EnsureBool(),
        ),
        validate_defaults=("dataset",),
        tailor_for_dataset=({"outfile": "dataset"}),
    )

    @staticmethod
    @datasetmethod(name="export_redcap_project_xml")
    @eval_results
    def __call__(
        url: str,
        outfile: Path,
        dataset: Optional[DatasetParameter] = None,
        credential: Optional[str] = None,
        metadata_only: bool = False,
        survey_fields: bool = True,
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
        api = ProjectInfo(
            url=url,
            token=credprops["secret"],
        )

        # perform the api query
        # note: not exporting files or data access groups
        response = api.export_project_xml(
            metadata_only=metadata_only,
            survey_fields=survey_fields,
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
                else _write_commit_message(
                    "Export REDCap Project XML",
                    metadata_only=metadata_only,
                    survey_fields=survey_fields,
                ),
                path=outfile,
            )

        # yield successful result if we made it to here
        yield get_status_dict(
            action="export_redcap_project_xml",
            path=outfile,
            status="ok",
        )


def _write_commit_message(header: str, **export_opts: str) -> str:
    """Return a formatted commit message that lists export options"""
    if len(export_opts) > 0:
        option_list = "\n".join([f"- {k}: {v}" for k, v in export_opts.items()])
        message = f"{header}\n\nExport options:\n{option_list}"
    else:
        message = header
    return message
