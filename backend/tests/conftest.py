import pytest

from techconnect_classes_api.core.config import get_settings
from techconnect_classes_api.core.log import setup_logger


@pytest.fixture(scope="session", autouse=True)
def test_logger():
    setup_logger()


@pytest.fixture(scope="session")
def test_settings():
    yield get_settings("test")
