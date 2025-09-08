import pytest
from unittest.mock import MagicMock

from techconnect_classes_api.core.config import get_settings
from techconnect_classes_api.core.log import setup_logger


@pytest.fixture(scope="session", autouse=True)
def test_logger():
    setup_logger()


@pytest.fixture(scope="session")
def test_settings():
    yield get_settings("test")


@pytest.fixture(autouse=True)
def patched_db_session(monkeypatch):
    """Mocks the database session"""
    mock_session = MagicMock()
    
    # Mock the get_local_session to return mock_session object
    mock_sessionmaker = MagicMock(return_value=mock_session)
    monkeypatch.setattr("techconnect_classes_api.database.get_local_session", mock_sessionmaker)
    
    yield mock_session
