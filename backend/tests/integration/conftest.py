import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from techconnect_classes_api.core.config import settings as _settings

TEST_DB_URL = f"postgresql://{_settings.POSTGRES_USER}:{_settings.POSTGRES_PASSWORD}@{_settings.POSTGRES_HOST}:{_settings.POSTGRES_PORT}/{_settings.POSTGRES_DB}"


@pytest.fixture(scope="session")
def _engine():
    yield create_engine(url=TEST_DB_URL, echo=False)


@pytest.fixture(scope="session")
def test_session(_engine):
    yield sessionmaker(bind=_engine, autocommit=False, autoflush=False)
