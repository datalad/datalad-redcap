from unittest.mock import patch

from datalad.api import export_redcap_form
from datalad.distribution.dataset import Dataset
from datalad_next.tests.utils import (
    assert_status,
    eq_,
)

CSV_CONTENT = "foo,bar,baz\nspam,spam,spam"


def test_export_writes_file(tmp_path, api_url, credman_filled):
    ds = Dataset(tmp_path).create(result_renderer="disabled")
    fname = "form.csv"

    with patch(
        "datalad_redcap.export_form.Records.export_records", return_value=CSV_CONTENT
    ):
        res = export_redcap_form(
            url=api_url,
            forms=["foo"],
            outfile=fname,
            dataset=ds,
        )

    # check that the command returned ok
    assert_status("ok", res)

    # check that the file was created and left in clean state
    eq_(ds.status(fname, return_type="item-or-list").get("state"), "clean")
