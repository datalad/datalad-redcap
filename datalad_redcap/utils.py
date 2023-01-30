"""Utility methods"""

import logging
from typing import Optional

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
