from __future__ import annotations

from loguru import logger
from sqlalchemy import select

from tms.auth.security import hash_password
from tms.domain import models
from tms.infra.config import settings
from tms.infra.database import SessionLocal


def ensure_default_admin() -> None:
    with SessionLocal() as session:
        result = session.execute(select(models.User).where(models.User.email == settings.default_admin_email)).scalar_one_or_none()
        if result:
            return
        logger.info("Creating default admin user %s", settings.default_admin_email)
        admin = models.User(
            email=settings.default_admin_email,
            full_name="Hawker Boys Admin",
            password_hash=hash_password(settings.default_admin_password),
            role=models.UserRoleEnum.ADMIN,
        )
        session.add(admin)
        session.commit()
