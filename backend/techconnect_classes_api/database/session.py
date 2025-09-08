from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker


def get_engine(database_url: str, echo: bool = False) -> Engine:
    return create_engine(url=database_url, echo=echo)


def get_local_session(database_url: str, echo: bool = False) -> sessionmaker:
    engine = get_engine(database_url, echo)
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)
