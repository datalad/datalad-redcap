def test_register():
    import datalad.api as da

    assert hasattr(da, "export_redcap_form")
    assert hasattr(da, "export_redcap_report")
    assert hasattr(da, "export_redcap_project_xml")
    assert hasattr(da, "redcap_query")
