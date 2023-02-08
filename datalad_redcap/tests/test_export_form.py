from unittest.mock import patch

from datalad.api import export_redcap_form
from datalad.distribution.dataset import Dataset
from datalad_next.tests.utils import (
    assert_status,
    eq_,
    with_credential,
    with_tempfile,
)

DUMMY_TOKEN = "WTJ3G8XWO9G8V1BB4K8N81KNGRPFJOVL"  # needed to pass length assertion
CSV_CONTENT = "foo,bar,baz\nspam,spam,spam"
CREDNAME = "redcap"


@with_tempfile
@patch("datalad_redcap.export_form.Records.export_records", return_value=CSV_CONTENT)
@with_credential(CREDNAME, type="token", secret=DUMMY_TOKEN)
def test_export_writes_file(ds_path=None, mocker=None):
    ds = Dataset(ds_path).create(result_renderer="disabled")
    fname = "form.csv"

    res = export_redcap_form(
        url="https://www.example.com/api/",
        forms=["foo"],
        outfile=fname,
        dataset=ds,
        credential=CREDNAME,
    )

    # check that the command returned ok
    assert_status("ok", res)

    # check that the file was created and left in clean state
    eq_(ds.status(fname, return_type="item-or-list").get("state"), "clean")
