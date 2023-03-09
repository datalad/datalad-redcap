import pytest

from datalad.conftest import setup_package
from datalad_next.credman import CredentialManager


@pytest.fixture
def api_url():
    """Yield a dummy API URL that passes assertions"""
    yield "https://www.example.com/api/"


@pytest.fixture
def credman_filled(api_url):
    """Yield a credential manager containing a dummy token

    The dummy token has the api_url as realm, allowing tests using the
    api_url fixture to implictitly have a valid credential. The token
    is 32 characters long to pass PyCap's assertion.
    """
    credman = CredentialManager()
    credman.set(
        name="pytest-redcap",
        type="token",
        secret="WTJ3G8XWO9G8V1BB4K8N81KNGRPFJOVL",
        realm=api_url,
    )
    yield credman
    credman.remove(name="pytest-redcap")
