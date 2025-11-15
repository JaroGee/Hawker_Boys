from __future__ import annotations

import datetime as dt
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from tms.auth.security import (
    create_access_token,
    hash_password,
    verify_password,
    require_admin,
    get_current_user,
)
from tms.domain import models
from tms.infra.database import get_db
from tms.schemas import Token, UserCreate, UserRead

router = APIRouter()


@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> Token:
    user = db.execute(
        models.User.__table__.select().where(models.User.email == form_data.username)
    ).mappings().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")

    db_user = db.get(models.User, uuid.UUID(user["id"]))
    assert db_user is not None  # for type checker

    if not verify_password(form_data.password, db_user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")

    db_user.last_login_at = dt.datetime.utcnow()
    db.commit()

    access_token = create_access_token(str(db_user.id), db_user.role.value)
    expires_minutes = int(dt.timedelta(minutes=30).total_seconds())
    return Token(access_token=access_token, expires_in=expires_minutes)


@router.post("/users", response_model=UserRead, dependencies=[Depends(require_admin)])
def create_user(user: UserCreate, db: Session = Depends(get_db)) -> UserRead:
    if db.execute(models.User.__table__.select().where(models.User.email == user.email)).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    db_user = models.User(
        email=user.email,
        full_name=user.full_name,
        password_hash=hash_password(user.password),
        role=models.UserRoleEnum(user.role),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return UserRead.model_validate(db_user)


@router.get("/me", response_model=UserRead)
def read_current_user(current_user: models.User = Depends(get_current_user)) -> UserRead:
    return UserRead.model_validate(current_user)
