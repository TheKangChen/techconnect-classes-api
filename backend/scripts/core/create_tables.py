from techconnect_classes.core.config import settings
from techconnect_classes.database import get_engine, get_sqlalchemy_db_url
from techconnect_classes.database.base_class import Base


def create_tables() -> None:
    database_url = get_sqlalchemy_db_url(settings)
    engine = get_engine(database_url)
    Base.metadata.create_all(bind=engine)
