from __future__ import annotations

import datetime as dt
import uuid

from pydantic import BaseModel


class EnrollmentCreate(BaseModel):
    learner_id: uuid.UUID
    class_run_id: uuid.UUID
    status: str = "registered"


class EnrollmentUpdate(BaseModel):
    status: str | None = None


class EnrollmentRead(BaseModel):
    id: uuid.UUID
    learner_id: uuid.UUID
    class_run_id: uuid.UUID
    status: str
    enrollment_date: dt.date
    ssg_enrollment_id: str | None
    created_at: dt.datetime
    updated_at: dt.datetime

    class Config:
        from_attributes = True
