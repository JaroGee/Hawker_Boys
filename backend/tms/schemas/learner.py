from __future__ import annotations

import uuid
from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr


class LearnerCreate(BaseModel):
    full_name: str
    email: Optional[EmailStr] = None
    contact_number: Optional[str] = None
    hashed_identifier: Optional[str] = None
    date_of_birth: Optional[date] = None


class LearnerUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    contact_number: Optional[str] = None
    date_of_birth: Optional[date] = None


class LearnerRead(BaseModel):
    id: uuid.UUID
    full_name: str
    email: Optional[EmailStr]
    contact_number: Optional[str]
    hashed_identifier: Optional[str]
    date_of_birth: Optional[date]

    class Config:
        from_attributes = True
