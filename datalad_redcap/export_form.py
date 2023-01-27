"""Export one or multiple forms"""

import os
from pathlib import Path
import textwrap
from typing import (
    List,
    Optional,
    Tuple,
    Union,
)

from redcap.methods.records import Records

from datalad.distribution.dataset import (
    Dataset,
    EnsureDataset,
    datasetmethod,
    require_dataset,
    resolve_path,
)
from datalad.interface.base import (
    Interface,
    build_doc,
)
from datalad.interface.common_opts import (
    nosave_opt,
    save_message_opt,
)
from datalad.interface.results import get_status_dict
from datalad.interface.utils import eval_results
from datalad.support.constraints import (
    EnsureNone,
    EnsureStr,
)
from datalad.support.param import Parameter

__docformat__ = "restructuredtext"


@build_doc
class ExportForm(Interface):
    """Export records from selected forms (instruments)

    This is an equivalent to "Selected Instruments" export option in
    REDCap's interface.  Allows saving response data from one or
    several forms into a single csv file.
    """

    _params_ = dict(
        url=Parameter(
            args=("url",),
            doc="API URL to a REDCap server",
            constraints=EnsureStr(),
        ),
        forms=Parameter(
            args=("forms",),
            doc="project form name(s)",
            constraints=EnsureStr(),
            nargs="+",
            metavar="form",
        ),
        outfile=Parameter(
            args=("outfile",),
            doc="file to write. Existing files will be overwritten.",
            constraints=EnsureStr(),
        ),
        dataset=Parameter(
            args=("-d", "--dataset"),
            metavar="PATH",
            doc="""the dataset in which the output file will be saved.
            The `outfile` argument will be interpreted as being relative to
            this dataset.  If no dataset is given, it will be identified
            based on the working directory.""",
            constraints=EnsureDataset() | EnsureNone(),
        ),
        message=save_message_opt,
        save=nosave_opt,
    )

    @staticmethod
    @datasetmethod(name="export_redcap_form")
    @eval_results
    def __call__(
        url: str,
        forms: List[str],
        outfile: str,
        dataset: Optional[Union[Dataset, str]] = None,
        message: Optional[str] = None,
        save: bool = True,
    ):

        # temporary solution: read token from env until we add authentication
        token = os.getenv("REDCAP_TOKEN")

        # work with a dataset, sort out paths
        ds = require_dataset(dataset)
        res_outfile = resolve_path(outfile, ds=ds)

        # refuse to operate if target file is outside the dataset or not clean
        ok_to_edit, unlock = _check_ok_to_edit(res_outfile, ds)
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

        # create an api object
        api = Records(
            url=url,
            token=token,
        )

        # perform the api query
        # outputs a string if format is csv, errors for an incorrect query
        response = api.export_records(
            format_type="csv",
            forms=forms,
        )

        # unlock the file if needed, and write contents
        if unlock:
            ds.unlock(res_outfile)
        with open(res_outfile, "wt") as f:
            f.write(response)

        # save changes in the dataset
        if save:
            ds.save(
                message=message
                if message is not None
                else _write_commit_message(forms),
                path=res_outfile,
            )

        # yield successful result if we made it to here
        yield get_status_dict(
            action="export_redcap_form",
            path=outfile,
            status="ok",
        )


def _check_ok_to_edit(filepath: Path, ds: Dataset) -> Tuple[bool, bool]:
    """Check if it's ok to write to a file, and if it needs unlocking

    Only allows paths that are within the given dataset (not outside, not in
    a subdatset) and lead either to existing clean files or nonexisting files.
    Uses ds.repo.status.
    """
    try:
        st = ds.repo.status(paths=[filepath])
    except ValueError:
        # path outside the dataset
        return False, False

    if st == {}:
        # path is fine, file doesn't exist
        ok_to_edit = True
        unlock = False
    else:
        st_fp = st[filepath]  # need to unpack
        if st_fp["type"] == "file" and st_fp["state"] == "clean":
            ok_to_edit = True
            unlock = False
        elif st_fp["type"] == "symlink" and st_fp["state"] == "clean":
            ok_to_edit = True
            unlock = True
        else:
            # note: paths pointing into subdatasets have type=dataset
            ok_to_edit = False
            unlock = False
    return ok_to_edit, unlock


def _write_commit_message(which_forms: List[str]) -> str:
    """Return a formatted commit message that includes form names"""
    forms = ", ".join(which_forms)
    header = "Export RedCap forms"
    body = "\n".join(textwrap.wrap(f"Contains the following forms: {forms}."))
    return header + "\n\n" + body
