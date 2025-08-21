import logging
from contextlib import contextmanager
from typing import Generator, TypeVar

from sqlalchemy import MetaData, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from techconnect_classes_api.core.config import Settings, settings

log = logging.getLogger(__name__)

POSTGRES_INDEXES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}

Base = declarative_base(
    metadata=MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)
)

ModelType = TypeVar("ModelType", bound=Base)


def get_sqlalchemy_db_url(_settings: Settings) -> str:
    return f"postgresql://{_settings.POSTGRES_USER}:{_settings.POSTGRES_PASSWORD}@{_settings.POSTGRES_HOST}:{_settings.POSTGRES_PORT}/{_settings.POSTGRES_DB}"


def get_engine(database_url: str, echo: bool = False) -> Engine:
    return create_engine(url=database_url, echo=echo)


def get_local_session(database_url: str, echo: bool = False) -> sessionmaker:
    engine = get_engine(database_url, echo)
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    log.debug("Getting database session")
    database_url = get_sqlalchemy_db_url(settings)
    session_local = get_local_session(database_url)
    db = session_local()
    try:
        yield db
    finally:
        log.debug("Closing database session")
        db.close()


@contextmanager
def get_managed_db() -> Generator:
    log.debug("Getting database session")
    database_url = get_sqlalchemy_db_url(settings)
    session_local = get_local_session(database_url)
    db = session_local()
    try:
        yield db
    finally:
        log.debug("Closing database session")
        db.close()
