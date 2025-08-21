from techconnect_classes_api.core.config import settings
from techconnect_classes_api.database import get_engine, get_sqlalchemy_db_url
from techconnect_classes_api.database.db import Base


def create_tables() -> None:
    database_url = get_sqlalchemy_db_url(settings)
    engine = get_engine(database_url)
    Base.metadata.create_all(bind=engine)
