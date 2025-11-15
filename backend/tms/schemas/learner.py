from __future__ import annotations

import datetime as dt
import uuid

from pydantic import BaseModel


class LearnerBase(BaseModel):
    given_name: str
    family_name: str
    date_of_birth: dt.date | None = None
    contact_number: str | None = None


class LearnerCreate(LearnerBase):
    masked_nric: str | None = None


class LearnerRead(LearnerBase):
    id: uuid.UUID
    masked_nric: str | None
    created_at: dt.datetime
    updated_at: dt.datetime

    class Config:
        from_attributes = True
