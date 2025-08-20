import logging
from techconnect_classes.core.log import setup_rich_logger
from argparse import ArgumentParser
from scripts.core.init_database import create_tables_and_seed_database


setup_rich_logger()
log = logging.getLogger(__name__)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--env",
        help="Environment for which to seed the database",
        default="dev",
        choices=["dev", "test"],
    )
    args = parser.parse_args()
    env = args.env
    log.info(f"Current environment: {env}")
    create_tables_and_seed_database(env)
    log.info("Database seeded")
