from pathlib import Path

from scripts.core.create_tables import create_tables
from scripts.core.seeding import seed_database

CLASS_INFO_FILE = (
    Path(__file__).resolve().parent.parent.parent
    / "resources"
    / "active_classes_250710.csv"
)


def create_tables_and_seed_database(env: str) -> None:
    create_tables()
    seed_database(env, CLASS_INFO_FILE)
