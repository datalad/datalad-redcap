from unittest.mock import patch

from datalad.api import export_redcap_report
from datalad.distribution.dataset import Dataset
from datalad_next.tests.utils import (
    assert_status,
    eq_,
    with_credential,
    with_tempfile,
)

TEST_TOKEN = "WTJ3G8XWO9G8V1BB4K8N81KNGRPFJOVL"  # needed to pass length assertion
CSV_CONTENT = "foo,bar,baz\nspam,spam,spam"
CREDNAME = "redcap"


@with_tempfile
@patch("datalad_redcap.export_report.Reports.export_report", return_value=CSV_CONTENT)
@with_credential(CREDNAME, type="token", secret=TEST_TOKEN)
def test_export_writes_file(ds_path=None, mocker=None):
    ds = Dataset(ds_path).create(result_renderer="disabled")
    fname = "report.csv"

    res = export_redcap_report(
        url="https://www.example.com/api/",
        report="1234",
        outfile=fname,
        dataset=ds,
        credential=CREDNAME,
    )

    # check that the command returned ok
    assert_status("ok", res)

    # check that the file was created and left in clean state
    eq_(ds.status(fname, return_type="item-or-list").get("state"), "clean")
