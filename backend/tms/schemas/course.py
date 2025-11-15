from __future__ import annotations

import datetime as dt
import uuid

from pydantic import BaseModel, Field


class ModuleCreate(BaseModel):
    title: str
    description: str | None = None
    order: int = 0


class ModuleRead(ModuleCreate):
    id: uuid.UUID


class CourseBase(BaseModel):
    code: str = Field(..., max_length=50)
    title: str = Field(..., max_length=255)
    description: str | None = None
    is_active: bool = True


class CourseCreate(CourseBase):
    modules: list[ModuleCreate] = []


class CourseUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    is_active: bool | None = None


class CourseRead(CourseBase):
    id: uuid.UUID
    ssg_course_code: str | None
    created_at: dt.datetime
    updated_at: dt.datetime
    modules: list[ModuleRead] = []

    class Config:
        from_attributes = True


class ClassRunBase(BaseModel):
    reference_code: str
    start_date: dt.date
    end_date: dt.date


class ClassRunCreate(ClassRunBase):
    status: str = "draft"


class ClassRunRead(ClassRunBase):
    id: uuid.UUID
    status: str
    ssg_run_id: str | None
    created_at: dt.datetime
    updated_at: dt.datetime

    class Config:
        from_attributes = True
