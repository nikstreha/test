from functools import cached_property
from typing import Literal

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Postgres
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB_NAME: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_ECHO: bool = False
    POSTGRES_ECHO_POOL: bool = False
    POSTGRES_POOL_SIZE: int = 5
    POSTGRES_MAX_OVERFLOW: int = 10

    # Password hasher
    PASSWORD_HASHER_CONCURRENCY_LIMIT: int = 4
    PASSWORD_HASHER_WAIT_TIMEOUT_S: float = 5.0
    PASSWORD_HASHER_THREAD_POOL_SIZE: int = 4
    PASSWORD_HASHER_PEPPER: str

    # Token provider
    TOKEN_SECRET_KEY: str
    TOKEN_ALGORITHM: str = "HS256"
    TOKEN_ACCESS_EXPIRE_MINUTE: int = 30
    TOKEN_REFRESH_EXPIRE_DAY: int = 7

    # Logging
    LOG_LEVEL: str = "INFO"

    # Rate limiting
    RATE_LIMIT_LOGIN_MAX_ATTEMPTS: int = 5
    RATE_LIMIT_LOGIN_WINDOW_SECONDS: int = 60

    # Cookie
    COOKIE_REFRESH_TOKEN_KEY: str = "refresh_token"
    COOKIE_SECURE: bool = True
    COOKIE_HTTPONLY: bool = True
    COOKIE_SAMESITE: Literal["lax", "strict", "none"] = "lax"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    @cached_property
    def postgres_dsn(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=self.POSTGRES_HOST,
                port=self.POSTGRES_PORT,
                path=self.POSTGRES_DB_NAME,
            )
        )
