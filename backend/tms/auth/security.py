from __future__ import annotations

import datetime as dt
import uuid
from typing import Iterable

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from tms.infra.config import settings
from tms.infra.database import get_db
from tms.domain import models
from tms.schemas import TokenPayload

pwd_context = CryptContext(schemes=[settings.password_hash_scheme], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


def create_access_token(subject: str, role: str, expires_delta: dt.timedelta | None = None) -> str:
    expire = dt.datetime.utcnow() + (
        expires_delta
        if expires_delta
        else dt.timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode = {"sub": subject, "role": role, "exp": expire}
    return jwt.encode(to_encode, settings.secret_key, algorithm="HS256")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


class RoleChecker:
    def __init__(self, allowed_roles: Iterable[models.UserRoleEnum]):
        self.allowed_roles = set(allowed_roles)

    def __call__(self, token: str = Depends(oauth2_scheme)) -> TokenPayload:
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
            token_data = TokenPayload(**payload)
        except JWTError as exc:  # pragma: no cover - defensive branch
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc

        if token_data.role not in {role.value for role in self.allowed_roles}:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")

        return token_data


require_admin = RoleChecker([models.UserRoleEnum.ADMIN])
require_ops_or_admin = RoleChecker([models.UserRoleEnum.ADMIN, models.UserRoleEnum.OPS])
require_trainer_or_admin = RoleChecker([models.UserRoleEnum.ADMIN, models.UserRoleEnum.TRAINER])


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> models.User:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        token_data = TokenPayload(**payload)
    except JWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc

    user = db.get(models.User, uuid.UUID(token_data.sub))
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive account")

    return user
