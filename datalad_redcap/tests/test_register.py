from datalad.tests.utils_pytest import assert_result_count


def test_register():
    import datalad.api as da
    assert hasattr(da, 'export_redcap_form')
    # assert_result_count(
    #     da.hello_cmd(),
    #     1,
    #     action='demo')

