from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from tms.infra.config import settings


class Base(DeclarativeBase):
    pass


def _create_engine():
    kwargs: dict[str, object] = {"future": True, "pool_pre_ping": True}
    if str(settings.database_url).startswith("sqlite"):
        kwargs["connect_args"] = {"check_same_thread": False}
    else:
        pool_size = getattr(settings, "db_pool_size", None)
        max_overflow = getattr(settings, "db_max_overflow", None)
        if pool_size:
            kwargs["pool_size"] = pool_size
        if max_overflow:
            kwargs["max_overflow"] = max_overflow
    return create_engine(str(settings.database_url), **kwargs)


def get_engine():
    return engine


def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def session_scope() -> Iterator[Session]:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


engine = _create_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
