from __future__ import annotations

import datetime as dt
import uuid

from pydantic import BaseModel

from .types import LocalEmailStr

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    role: str


class TokenPayload(BaseModel):
    sub: str
    role: str
    exp: int


class LoginRequest(BaseModel):
    email: LocalEmailStr
    password: str


class UserBase(BaseModel):
    email: LocalEmailStr
    full_name: str


class UserCreate(UserBase):
    password: str
    role: str


class UserRead(UserBase):
    id: uuid.UUID
    role: str
    is_active: bool
    last_login_at: dt.datetime | None

    class Config:
        from_attributes = True
