import pytest
from utils.sessions import SoapSession


@pytest.fixture(scope='module')
def soap_session(envs):
    session = SoapSession(soap_url=envs.soap_url)
    return session
