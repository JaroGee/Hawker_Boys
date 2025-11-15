from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Hawker Boys TMS"
    environment: Literal["local", "staging", "production"] = "local"
    secret_key: str = "change-me"
    access_token_expire_minutes: int = 60

    database_url: str = "sqlite:///./tms_dev.db"
    db_pool_size: int = 5
    db_max_overflow: int = 10

    redis_url: str = "redis://localhost:6379/0"

    ssg_base_url: str = "https://sandbox-developer.ssg-wsg.gov.sg"
    ssg_client_id: str = ""
    ssg_client_secret: str = ""
    ssg_timeout_seconds: int = 30
    ssg_env: Literal["sandbox", "production"] = "sandbox"
    ssg_webhook_secret: str | None = None

    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
