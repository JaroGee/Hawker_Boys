from __future__ import annotations

import sys

import httpx
from loguru import logger
from sqlalchemy import text

from tms.infra.config import settings
from tms.infra.database import engine

REQUIRED_VARS = [
    "SECRET_KEY",
    "DATABASE_URL",
    "REDIS_URL",
    "SSG_BASE_URL",
    "SSG_CLIENT_ID",
    "SSG_CLIENT_SECRET",
    "SSG_WEBHOOK_SECRET",
]


def check_env() -> None:
    missing = [var for var in REQUIRED_VARS if not getattr(settings, var.lower())]
    if missing:
        raise RuntimeError(f"Missing environment variables: {', '.join(missing)}")


def check_database() -> None:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))


def check_ssg_token() -> None:
    try:
        response = httpx.post(
            f"{settings.ssg_base_url}/oauth2/token",
            data={
                "client_id": settings.ssg_client_id,
                "client_secret": settings.ssg_client_secret,
                "grant_type": "client_credentials",
            },
            timeout=settings.ssg_timeout_seconds,
        )
        response.raise_for_status()
        logger.info("SSG token retrieval OK")
    except Exception as exc:  # pragma: no cover - environment dependent
        logger.warning("SSG token check skipped or failed: %s", exc)


def main() -> None:
    try:
        check_env()
        logger.info("Environment variables loaded")
        check_database()
        logger.info("Database connectivity OK")
        check_ssg_token()
        logger.info("Preflight completed")
    except Exception as exc:  # pragma: no cover - CLI script
        logger.error("Preflight failed: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
