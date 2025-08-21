import logging
import os

from pydantic_settings import BaseSettings, SettingsConfigDict

log = logging.getLogger(__name__)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="./.env.dev", env_file_encoding="utf-8", case_sensitive=True
    )

    ENV: str
    LOG_LEVEL: str

    SERVER_HOST: str
    SERVER_PORT: int

    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int


class DevSettings(Settings):
    model_config = SettingsConfigDict(
        env_file="./.env.dev", env_file_encoding="utf-8", case_sensitive=True
    )
    ENV: str = "dev"


class TestSettings(Settings):
    model_config = SettingsConfigDict(
        env_file="./.env.test", env_file_encoding="utf-8", case_sensitive=True
    )
    ENV: str = "test"


def get_setting(env: str = "dev") -> Settings:
    log.debug(f"Getting settings for env: {env}")
    if env.lower() in ["dev", "development"]:
        return DevSettings()
    if env.lower() in ["test", "testing"]:
        return TestSettings()
    raise ValueError("Invalid environment. Must be 'dev' or 'test'.")


_env = os.environ.get("ENV", "dev")

settings = get_setting(env=_env)
