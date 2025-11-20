from __future__ import annotations

import datetime as dt

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
from tms.schemas import LoginRequest, Token, UserCreate, UserRead

router = APIRouter()


def _authenticate_user(db: Session, email: str, password: str) -> models.User:
    user = db.execute(
        models.User.__table__.select().where(models.User.email == email)
    ).mappings().first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")

    db_user = db.get(models.User, user["id"])
    assert db_user is not None  # for type checker

    if not verify_password(password, db_user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
    return db_user


def _issue_token(db: Session, db_user: models.User) -> Token:
    db_user.last_login_at = dt.datetime.utcnow()
    db.commit()

    access_token = create_access_token(str(db_user.id), db_user.role.value)
    expires_minutes = int(dt.timedelta(minutes=30).total_seconds())
    return Token(access_token=access_token, expires_in=expires_minutes, role=db_user.role.value)


@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> Token:
    user = _authenticate_user(db, form_data.username, form_data.password)
    return _issue_token(db, user)


@router.post("/login", response_model=Token)
def login_with_json(payload: LoginRequest, db: Session = Depends(get_db)) -> Token:
    user = _authenticate_user(db, payload.email, payload.password)
    return _issue_token(db, user)


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
