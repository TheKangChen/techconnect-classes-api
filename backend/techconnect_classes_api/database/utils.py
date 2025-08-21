from sqlalchemy import inspect
from sqlalchemy.engine import Engine
import logging

log = logging.getLogger(__name__)


def show_tables(engine: Engine, table: str | None = None, include_all: bool = True):
    inspector = inspect(engine)

    if include_all:
        table_names = inspector.get_table_names()
        log.info("Tables in database:")
        for t in table_names:
            log.info("    ", t)

    if table:
        columns = inspector.get_columns(table)
        log.info(f"Columns in '{table}':")
        for column in columns:
            log.info("    ", column["name"])
