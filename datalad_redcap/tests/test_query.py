from unittest.mock import patch

from datalad.api import redcap_query
from datalad_next.tests.utils import (
    assert_result_count,
    with_credential,
)

DUMMY_URL = "https://www.example.com/api/"
DUMMY_TOKEN = "WTJ3G8XWO9G8V1BB4K8N81KNGRPFJOVL"  # needed to pass length assertion
JSON_CONTENT = {"foo": "bar"}
CREDNAME = "redcap"


@patch(
    "datalad_redcap.query.MyInstruments.export_instruments", return_value=JSON_CONTENT
)
@with_credential(CREDNAME, type="token", secret=DUMMY_TOKEN)
def test_redcap_query_has_result(mocker=None):
    assert_result_count(
        redcap_query(url=DUMMY_URL, credential=CREDNAME, result_renderer="disabled"), 1
    )
