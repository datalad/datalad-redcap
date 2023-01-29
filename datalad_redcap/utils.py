"""Utility methods"""

import logging
from typing import Optional

from datalad_next.exceptions import CapturedException
from datalad_next.utils import CredentialManager

lgr = logging.getLogger("datalad.redcap.utils")


def update_credentials(
    credman: CredentialManager, credname: Optional[str], credprops: dict
) -> None:
    """Update credentials, generating default name if needed"""
    if credname is None:
        # no name given upfront, and none found - create default
        credname = "{kind}{delim}{realm}".format(
            kind="redcap",
            delim="-" if "realm" in credprops else "",
            realm=credprops.get("realm", ""),
        )
        # do not override if the name is already in use
        if credman.get(name=credname) is not None:
            lgr.warning(
                "The entered credential will not be stored, "
                "a credential with the default name %r already exists.",
                credname,
            )
            return
    try:
        # save a new credential or update last used date
        credman.set(credname, _lastused=True, **credprops)
    except Exception as e:
        # deescalate errors from credential storage
        lgr.warn(
            "Exception raised when storing credential %r %r: %s",
            credname,
            credprops,
            CapturedException(e),
        )
