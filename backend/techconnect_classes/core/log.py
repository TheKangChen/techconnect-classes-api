import logging
import sys
from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import BaseModel
from rich.logging import RichHandler

from techconnect_classes.core.config import settings

# Configure the basic logging system
FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

LOGGER_FILE = Path(settings.LOGGER_FILE)
DATE_FORMAT = "%d %b %Y | %H:%M:%S"
LOGGER_FORMAT = "%(asctime)s | %(message)s"


class LoggerConfig(BaseModel):
    handlers: list
    format: str | None
    date_format: str | None = None
    logger_file: Path | None = None
    level: int = logging.INFO


@lru_cache
def get_logger_config() -> LoggerConfig:
    handler_format = logging.Formatter(LOGGER_FORMAT, datefmt=DATE_FORMAT)

    output_file_handler = logging.FileHandler(LOGGER_FILE)
    output_file_handler.setFormatter(handler_format)

    if settings.ENV.lower() in ["dev", "development", "test", "testing"]:
        from rich.logging import RichHandler

        return LoggerConfig(
            handlers=[
                RichHandler(
                    rich_tracebacks=True, tracebacks_show_locals=True, show_time=False
                ),
                output_file_handler,
            ],
            format=None,
            date_format=DATE_FORMAT,
            logger_file=LOGGER_FILE,
        )

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(handler_format)

    return LoggerConfig(
        handlers=[stdout_handler, output_file_handler],
        format="%(levelname)s: %(asctime)s \t%(message)s",
        date_format="%d-%b-%y %H:%M:%S",
        logger_file=LOGGER_FILE,
    )


def setup_rich_logger() -> None:
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    log_config = get_logger_config()

    logging.basicConfig(
        level=log_config.level,
        format=log_config.format,
        datefmt=log_config.date_format,
        handlers=log_config.handlers,
    )
