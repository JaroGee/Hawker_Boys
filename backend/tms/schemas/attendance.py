from __future__ import annotations

import datetime as dt
import uuid

from pydantic import BaseModel


class AttendanceCreate(BaseModel):
    enrollment_id: uuid.UUID
    session_id: uuid.UUID
    status: str
    remarks: str | None = None


class AttendanceRead(AttendanceCreate):
    id: uuid.UUID
    submitted_to_ssg: bool
    created_at: dt.datetime
    updated_at: dt.datetime

    class Config:
        from_attributes = True
