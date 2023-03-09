"""Tests related to parameter handling

These test for ValueError being raised in example situations related
to parameter validation, and should help ensure that parameter
validation works as expected. The export_records command is used as an
example command, and we still mock the api calls and provide a dummy
credential to let the command run if validation doesn't complain.
"""

import pytest
from unittest.mock import patch

from datalad.api import export_redcap_form
from datalad.distribution.dataset import Dataset

from datalad_next.utils import chpwd

CSV_CONTENT = "foo,bar,baz\nspam,spam,spam"


def test_url_rejected(tmp_path, credman_filled, api_url):
    """Test that bad-form urls are rejected by validation"""

    credname, _ = credman_filled.query(realm=api_url)[0]
    ds = Dataset(tmp_path).create(result_renderer="disabled")

    with pytest.raises(ValueError):
        with patch(
            "datalad_redcap.export_form.Records.export_records",
            return_value=CSV_CONTENT,
        ):
            export_redcap_form(
                url="example.com",  # missing scheme, path
                forms=["foo"],
                outfile="foo.csv",
                dataset=ds,
                credential=credname,
            )


def test_dataset_not_found(tmp_path, credman_filled, api_url):
    """Test that nonexistent dataset is rejected by validation"""

    # explicit path that isn't a dataset
    with pytest.raises(ValueError):
        with patch(
            "datalad_redcap.export_form.Records.export_records",
            return_value=CSV_CONTENT,
        ):
            export_redcap_form(
                url=api_url,
                forms=["foo"],
                outfile="foo",
                dataset=tmp_path,
            )

    # no path given, pwd is not a dataset
    with chpwd(tmp_path, mkdir=True):
        with pytest.raises(ValueError):
            with patch(
                "datalad_redcap.export_form.Records.export_records",
                return_value=CSV_CONTENT,
            ):
                export_redcap_form(
                    url=api_url,
                    forms=["foo"],
                    outfile="foo",
                )
