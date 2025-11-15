from __future__ import annotations

from typing import Generator

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from tms.auth.authz import Role, authorize
from tms.infra.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def require_role(*roles: Role):
    def dependency(current_role: Role = Depends(authorize)) -> Role:
        if current_role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have access to this resource.")
        return current_role

    return dependency
