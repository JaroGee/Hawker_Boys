from __future__ import annotations

import datetime as dt
import uuid

from pydantic import BaseModel


class AssessmentCreate(BaseModel):
    enrollment_id: uuid.UUID
    score: int
    remarks: str | None = None
    assessed_on: dt.date | None = None


class AssessmentRead(AssessmentCreate):
    id: uuid.UUID
    assessed_on: dt.date
    created_at: dt.datetime
    updated_at: dt.datetime

    class Config:
        from_attributes = True
