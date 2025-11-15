from __future__ import annotations

from sqlalchemy import text

from tms.infra.database import SessionLocal
from tms.settings import settings


def check_database() -> None:
    try:
        with SessionLocal() as session:
            session.execute(text("SELECT 1"))
    except Exception as exc:  # noqa: BLE001
        raise SystemExit(f"Database connection failed: {exc}")


def check_settings() -> None:
    required = ["secret_key", "database_url", "redis_url", "ssg_base_url", "ssg_client_id"]
    missing = [name for name in required if not getattr(settings, name)]
    if missing:
        raise SystemExit(f"Missing required settings: {', '.join(missing)}")


def check_filesystem() -> None:
    pass


def run() -> None:
    check_settings()
    check_database()
    check_filesystem()
    print("Preflight check passed.")


if __name__ == "__main__":
    run()
