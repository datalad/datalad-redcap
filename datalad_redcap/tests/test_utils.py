from datalad.distribution.dataset import Dataset

from datalad_redcap.utils import check_ok_to_edit


def test_check_ok_to_edit(tmp_path):
    """Tests whether location/state is correctly recognized"""
    ds = Dataset(tmp_path / "ds").create(result_renderer="disabled")
    subds = ds.create("subds", result_renderer="disabled")

    outside = tmp_path / "file_outside"
    inside = tmp_path / "ds" / "ds_file"
    below = tmp_path / "ds" / "subds" / "subds_file"

    outside.write_text("dummy")
    inside.write_text("dummy")
    below.write_text("dummy")

    ds.save(recursive=True)

    # outside is not ok
    ok2ed, _ = check_ok_to_edit(outside, ds)
    assert not ok2ed

    # inside is ok
    ok2ed, _ = check_ok_to_edit(inside, ds)
    assert ok2ed

    # subdataset is not ok
    ok2ed, _ = check_ok_to_edit(below, ds)
    assert not ok2ed

    # file with unsaved changes is not ok
    ds.unlock(inside)
    inside.write_text("new dummy")
    ok2ed, _ = check_ok_to_edit(inside, ds)
    assert not ok2ed
