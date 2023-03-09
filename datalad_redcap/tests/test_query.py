from unittest.mock import patch

from datalad.api import redcap_query
from datalad_next.tests.utils import (
    assert_result_count,
    with_credential,
)

JSON_CONTENT = {"foo": "bar"}


def test_redcap_query_has_result(credman_filled, api_url):
    with patch("datalad_redcap.query.MyInstruments.export_instruments", return_value=JSON_CONTENT):
        assert_result_count(
            redcap_query(url=api_url, result_renderer="disabled"), 1
        )
