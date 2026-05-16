import os
from datetime import timedelta

import tomllib
from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_MACHINE_EXPIRY: timedelta = timedelta(minutes=15)
CONFIG_FILE: str = "config.toml"

ONLY_OS_ENV: bool = os.getenv("NO_CONFIG_FILE") is not None


class RssConfig(BaseSettings):
    title: str
    link: str
    description: str


class DbConfig(BaseSettings):
    driver: str = "postgresql"
    username: str
    database: str
    password: str
    host: str
    port: int


class ApiConfig(BaseSettings):
    recovery_token: str | None


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__")

    rss: RssConfig | None = None
    db: DbConfig
    api: ApiConfig
    debug: bool = False


CONFIG: Config
if not ONLY_OS_ENV:
    with open(CONFIG_FILE, "rb") as f:
        preexisting: dict = tomllib.load(f)
        CONFIG = Config(**preexisting)
else:
    CONFIG = Config()
