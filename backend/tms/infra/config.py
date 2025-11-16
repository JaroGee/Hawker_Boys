from __future__ import annotations

from functools import lru_cache

from pydantic import AnyUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=['.env','../.env'], env_file_encoding='utf-8', case_sensitive=False, extra='ignore')
    app_env: str = Field("local", alias="APP_ENV")
    app_name: str = Field("Hawker Boys TMS", alias="APP_NAME")
    api_host: str = Field("0.0.0.0", alias="API_HOST")
    api_port: int = Field(8000, alias="API_PORT")
    secret_key: str = Field(..., alias="SECRET_KEY")
    access_token_expire_minutes: int = Field(30, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_minutes: int = Field(4320, alias="REFRESH_TOKEN_EXPIRE_MINUTES")
    password_hash_scheme: str = Field("bcrypt", alias="PASSWORD_HASH_SCHEME")
    log_level: str = Field("INFO", alias="LOG_LEVEL")
    frontend_origin: str | None = Field(None, alias="FRONTEND_ORIGIN")

    database_url: AnyUrl = Field(..., alias="DATABASE_URL")

    redis_url: AnyUrl = Field(..., alias="REDIS_URL")
    rq_default_queue: str = Field("ssg_sync", alias="RQ_DEFAULT_QUEUE")
    rq_worker_concurrency: int = Field(2, alias="RQ_WORKER_CONCURRENCY")

    ssg_base_url: AnyUrl = Field(..., alias="SSG_BASE_URL")
    ssg_client_id: str = Field(..., alias="SSG_CLIENT_ID")
    ssg_client_secret: str = Field(..., alias="SSG_CLIENT_SECRET")
    ssg_timeout_seconds: int = Field(30, alias="SSG_TIMEOUT_SECONDS")
    ssg_env: str = Field("sandbox", alias="SSG_ENV")
    ssg_webhook_secret: str = Field(..., alias="SSG_WEBHOOK_SECRET")

    default_admin_email: str = Field(..., alias="DEFAULT_ADMIN_EMAIL")
    default_admin_password: str = Field(..., alias="DEFAULT_ADMIN_PASSWORD")

    sentry_dsn: str | None = Field(None, alias="SENTRY_DSN")
@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
