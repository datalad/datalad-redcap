from unittest.mock import patch

from datalad.api import export_redcap_project_xml
from datalad.distribution.dataset import Dataset
from datalad_next.tests.utils import (
    assert_status,
    eq_,
)
from datalad.tests.utils_pytest import ok_file_has_content

XML_CONTENT = """<?xml version="1.0" encoding="UTF-8" ?>"""


def test_export_xml_saves_content(tmp_path, api_url, credman_filled):
    ds = Dataset(tmp_path).create(result_renderer="disabled")
    fname = "project.xml"

    with patch(
        "datalad_redcap.export_project_xml.ProjectInfo.export_project_xml",
        return_value=XML_CONTENT,
    ):
        res = export_redcap_project_xml(
            url=api_url,
            outfile=fname,
            dataset=ds,
        )

    assert_status("ok", res)
    ok_file_has_content(tmp_path.joinpath(fname), XML_CONTENT)
    eq_(ds.status(fname, return_type="item-or-list").get("state"), "clean")
