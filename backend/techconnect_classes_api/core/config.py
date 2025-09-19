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
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

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


class LocalDevSettings(Settings):
    model_config = SettingsConfigDict(
        env_file="./.env.local", env_file_encoding="utf-8", case_sensitive=True
    )
    ENV: str = "local"

def get_settings(env: str = "dev") -> Settings:
    log.debug(f"Getting settings for env: {env}")
    if env.lower() in ["dev", "development"]:
        return DevSettings()
    if env.lower() in ["test", "testing"]:
        return TestSettings()
    if env.lower() in ["local"]:
        return LocalDevSettings()
    raise ValueError("Invalid environment. Must be 'dev' or 'test'.")


_env = os.environ.get("ENV", "dev")

settings = get_settings(env=_env)
