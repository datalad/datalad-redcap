from pathlib import Path

from datalad.distribution.dataset import Dataset
from datalad_next.tests.utils import with_tempfile

from datalad_redcap.utils import check_ok_to_edit

@with_tempfile
def test_check_ok_to_edit(path=None):
    """Tests whether location/state is correctly recognized"""
    basedir = Path(path)
    ds = Dataset(basedir / "ds").create(result_renderer="disabled")
    subds = ds.create("subds", result_renderer="disabled")

    outside = basedir / "file_outside"
    inside = basedir / "ds" / "ds_file"
    below = basedir / "ds" / "subds" / "subds_file"

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
