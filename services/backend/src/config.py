import logging
import os
import re
from datetime import timedelta

import requests
import tomllib
from pydantic import BaseModel, Field, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_MACHINE_EXPIRY: timedelta = timedelta(minutes=15)
CONFIG_FILE: str = "config.toml"

ONLY_OS_ENV: bool = os.getenv("NO_CONFIG_FILE") is not None

_SLASH_DEDUPE: re.Pattern = re.compile("/+")


class RssConfig(BaseModel):
    title: str
    link: str
    description: str


class DbConfig(BaseModel):
    driver: str = "postgresql"
    username: str
    database: str
    password: str
    host: str
    port: int


class ApiConfig(BaseModel):
    recovery_token: str | None


class OidcConfig(BaseModel):
    issuer: HttpUrl
    client_id: str
    scopes: str = "openid profile email"
    private__well_known_url: HttpUrl | None = Field(
        alias="well_known_url", default=None
    )
    private__authorization_endpoint: HttpUrl | None = Field(
        alias="authorization_endpoint", default=None
    )
    private__token_endpoint: HttpUrl | None = Field(
        alias="token_endpoint", default=None
    )
    # _revocation_endpoint: HttpUrl | None = Field(alias="revocation_endpoint", default=None)
    private__end_session_endpoint: HttpUrl | None = Field(
        alias="end_session_endpoint", default=None
    )
    private__jwks_uri: HttpUrl | None = Field(alias="jwks_uri", default=None)

    @property
    def well_known_url(self) -> HttpUrl:
        if self.private__well_known_url is not None:
            return self.private__well_known_url
        return HttpUrl(
            str(self.issuer).rstrip("/") + "/.well-known/openid-configuration"
        )

    def model_post_init(self, __context):
        well_known: dict = {}

        # Try get well-known config
        logging.error(self.well_known_url)
        r: requests.Response = requests.get(str(self.well_known_url))
        logging.error("After")
        if r.ok:
            # If the URL is there and readable, convert to JSON
            # Fine to throw error if this fails, this URL should
            # have a standard JSON response
            well_known = r.json()

        # This ensures all values are covered
        # Allows us to confidently create properties that
        # do not return None.
        for key in (
            "authorization_endpoint",
            "token_endpoint",
            "end_session_endpoint",
            "jwks_uri",
        ):
            value: HttpUrl | None = getattr(self, "private__" + key)
            if value is None:
                if key in well_known:
                    print(self, key, well_known[key])
                    setattr(self, "private__" + key, well_known[key])
                else:
                    raise ValueError(
                        f"Could not find '{key}' under OIDC config. Either '{self.well_known_url}' does not resolve or does not contain this value. Please specify manually or fix well-known URL."
                    )

    @property
    def authorization_endpoint(self) -> HttpUrl:
        assert self.private__authorization_endpoint is not None
        return self.private__authorization_endpoint

    @property
    def token_endpoint(self) -> HttpUrl:
        assert self.private__token_endpoint is not None
        return self.private__token_endpoint

    @property
    def end_session_endpoint(self) -> HttpUrl:
        assert self.private__end_session_endpoint is not None
        return self.private__end_session_endpoint

    @property
    def jwks_uri(self) -> HttpUrl:
        assert self.private__jwks_uri is not None
        return self.private__jwks_uri


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__")

    site_root: HttpUrl
    backend_path: str = "/api"
    rss: RssConfig | None = None
    db: DbConfig
    api: ApiConfig
    oidc: OidcConfig | None = None
    session_secret: str
    debug: bool = False

    @property
    def api_root(self) -> str:
        # Something like '/testing///path//' should end up as 'testing/path'
        offset: str = re.sub(_SLASH_DEDUPE, "/", self.backend_path.strip("/"))
        return str(self.site_root) + "/" + offset + "/"


CONFIG: Config
if not ONLY_OS_ENV:
    with open(CONFIG_FILE, "rb") as f:
        preexisting: dict = tomllib.load(f)
        CONFIG = Config(**preexisting)
else:
    CONFIG = Config()  # pyright: ignore[reportCallIssue]
