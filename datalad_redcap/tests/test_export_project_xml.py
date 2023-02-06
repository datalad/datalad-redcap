from pathlib import Path
from unittest.mock import patch

from datalad.api import export_redcap_project_xml
from datalad.distribution.dataset import Dataset
from datalad_next.tests.utils import (
    assert_status,
    eq_,
    with_credential,
    with_tempfile,
)
from datalad.tests.utils_pytest import ok_file_has_content

DUMMY_URL = "https://www.example.com/api/"
DUMMY_TOKEN = "WTJ3G8XWO9G8V1BB4K8N81KNGRPFJOVL"  # needed to pass length assertion
XML_CONTENT = """<?xml version="1.0" encoding="UTF-8" ?>"""
CREDNAME = "redcap"


@with_tempfile
@patch(
    "datalad_redcap.export_project_xml.ProjectInfo.export_project_xml",
    return_value=XML_CONTENT,
)
@with_credential(CREDNAME, type="token", secret=DUMMY_TOKEN)
def test_export_xml_saves_content(ds_path=None, mocker=None):
    ds = Dataset(ds_path).create(result_renderer="disabled")
    fname = "project.xml"

    res = export_redcap_project_xml(
        url=DUMMY_URL,
        outfile=fname,
        dataset=ds,
        credential=CREDNAME,
    )

    assert_status("ok", res)
    ok_file_has_content(Path(ds_path).joinpath(fname), XML_CONTENT)
    eq_(ds.status(fname, return_type="item-or-list").get("state"), "clean")
