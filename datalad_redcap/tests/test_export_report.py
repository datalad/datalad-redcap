from unittest.mock import patch

from datalad.api import export_redcap_report
from datalad.distribution.dataset import Dataset
from datalad_next.tests.utils import (
    assert_status,
    eq_,
)

CSV_CONTENT = "foo,bar,baz\nspam,spam,spam"


def test_export_writes_file(tmp_path, api_url, credman_filled):
    ds = Dataset(tmp_path).create(result_renderer="disabled")
    fname = "report.csv"

    with patch(
        "datalad_redcap.export_report.Reports.export_report", return_value=CSV_CONTENT
    ):
        res = export_redcap_report(
            url=api_url,
            report="1234",
            outfile=fname,
            dataset=ds,
        )

    # check that the command returned ok
    assert_status("ok", res)

    # check that the file was created and left in clean state
    eq_(ds.status(fname, return_type="item-or-list").get("state"), "clean")
