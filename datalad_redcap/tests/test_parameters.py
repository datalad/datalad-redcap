"""Tests related to parameter handling

These test for ValueError being raised in example situations related
to parameter validation, and should help ensure that parameter
validation works as expected. The export_records command is used as an
example command, and we still mock the api calls to let the command
run if validation doesn't complain.
"""

import pytest
from unittest.mock import patch

from datalad.api import export_redcap_form
from datalad.distribution.dataset import Dataset

from datalad_next.tests.utils import (
    with_credential,
    with_tempfile,
)
from datalad_next.utils import chpwd

TEST_TOKEN = "WTJ3G8XWO9G8V1BB4K8N81KNGRPFJOVL"  # needed to pass length assertion
CSV_CONTENT = "foo,bar,baz\nspam,spam,spam"
CREDNAME = "redcap"


@with_tempfile
@patch("datalad_redcap.export_form.Records.export_records", return_value=CSV_CONTENT)
@with_credential(CREDNAME, type="token", secret=TEST_TOKEN)
def test_url_rejected(ds_path=None, mocker=None):
    """Test that bad-form urls are rejected by validation"""
    ds = Dataset(ds_path).create(result_renderer="disabled")
    with pytest.raises(ValueError):
        export_redcap_form(
            url="example.com",  # missing scheme, path
            forms=["foo"],
            outfile="foo.csv",
            dataset=ds,
            credential=CREDNAME,
        )


@with_tempfile
@with_credential(CREDNAME, type="token", secret=TEST_TOKEN)
@patch("datalad_redcap.export_form.Records.export_records", return_value=CSV_CONTENT)
def test_dataset_not_found(path=None, mocker=None):
    """Test that nonexistent dataset is rejected by validation"""

    # explicit path that isn't a dataset
    with pytest.raises(ValueError):
        export_redcap_form(
            url="https://example.com/api",
            forms=["foo"],
            outfile="foo",
            dataset=path,
            credential=CREDNAME,
        )

    # no path given, pwd is not a dataset
    with chpwd(path, mkdir=True):
        with pytest.raises(ValueError):
            export_redcap_form(
                url="https://example.com/api",
                forms=["foo"],
                outfile="foo",
                credential=CREDNAME,
            )
