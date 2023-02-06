"""Utility methods"""

import logging
from pathlib import Path
from typing import(
    Optional,
    Tuple,
)

from datalad.distribution.dataset import Dataset
from datalad_next.exceptions import CapturedException
from datalad_next.utils import CredentialManager

lgr = logging.getLogger("datalad.redcap.utils")


def update_credentials(
    credman: CredentialManager, credname: Optional[str], credprops: dict
) -> None:
    """Update credentials, prompting for name if needed

    Saves a new credential or just updates last used date. Uses
    CredentialManager.set(), deescalating errors to warnings. Suggests
    "redcap-<api url>" as default name.
    """
    try:
        credman.set(
            name=credname,
            _lastused=True,
            _suggested_name="redcap{delim}{realm}".format(
                delim="-" if "realm" in credprops else "",
                realm=credprops.get("realm", ""),
            ),
            _context="for REDCap API access",
            **credprops,
        )
    except Exception as e:
        msg = ("Exception raised when storing credential %r %r: %s",)
        lgr.warn(msg, credname, credprops, CapturedException(e))


def check_ok_to_edit(filepath: Path, ds: Dataset) -> Tuple[bool, bool]:
    """Check if it's ok to write to a file, and if it needs unlocking

    Only allows paths that are within the given dataset (not outside, not in
    a subdatset) and lead either to existing clean files or nonexisting files.
    Uses ds.repo.status.
    """
    try:
        st = ds.repo.status(paths=[filepath])
    except ValueError:
        # path outside the dataset
        return False, False

    if st == {}:
        # path is fine, file doesn't exist
        ok_to_edit = True
        unlock = False
    else:
        st_fp = st[filepath]  # need to unpack
        if st_fp["type"] == "file" and st_fp["state"] == "clean":
            ok_to_edit = True
            unlock = False
        elif st_fp["type"] == "symlink" and st_fp["state"] == "clean":
            ok_to_edit = True
            unlock = True
        else:
            # note: paths pointing into subdatasets have type=dataset
            ok_to_edit = False
            unlock = False
    return ok_to_edit, unlock
