import logging
import os
from argparse import ArgumentParser

from scripts.core.drop_tables import drop_tables
from scripts.core.init_database import create_tables_and_seed_database
from techconnect_classes_api.core.log import setup_logger

setup_logger()
log = logging.getLogger(__name__)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--env",
        help="Environment for which to seed the database",
        default=os.environ.get("ENV", "local"),

        choices=["dev", "test", "local"],
    )
    parser.add_argument(
        "--drop-all",
        help="Drop all tables in database before seeding",
        action="store_true",
    )

    args = parser.parse_args()
    env = args.env
    drop_all = args.drop_all
    log.info(f"Current environment: {env}")
    if drop_all:
        log.info("Dropping all tables in database")
        drop_tables()

    create_tables_and_seed_database(env)
    log.info("Database seeded")
