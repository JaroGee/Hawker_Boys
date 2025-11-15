from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class SessionCreate(BaseModel):
    module_id: Optional[uuid.UUID] = None
    session_date: date
    start_time: datetime
    end_time: datetime


class SessionRead(SessionCreate):
    id: uuid.UUID

    class Config:
        from_attributes = True


class ClassRunCreate(BaseModel):
    course_id: uuid.UUID
    code: str
    start_date: date
    end_date: date
    capacity: int
    location: Optional[str] = None
    sessions: list[SessionCreate] = []


class ClassRunUpdate(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    capacity: Optional[int] = None
    location: Optional[str] = None
    ssg_run_id: Optional[str] = None


class ClassRunRead(BaseModel):
    id: uuid.UUID
    course_id: uuid.UUID
    code: str
    start_date: date
    end_date: date
    capacity: int
    location: Optional[str] = None
    ssg_run_id: Optional[str] = None
    sessions: list[SessionRead] = []

    class Config:
        from_attributes = True
