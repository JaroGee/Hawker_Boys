from __future__ import annotations

import uuid
from typing import Optional

from pydantic import BaseModel, Field


class CourseModuleCreate(BaseModel):
    code: str
    title: str
    description: Optional[str] = None
    duration_hours: int = Field(gt=0)


class CourseModuleRead(CourseModuleCreate):
    id: uuid.UUID

    class Config:
        from_attributes = True


class CourseCreate(BaseModel):
    code: str
    title: str
    description: Optional[str] = None
    modules: list[CourseModuleCreate] = []


class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_published: Optional[bool] = None


class CourseRead(BaseModel):
    id: uuid.UUID
    code: str
    title: str
    description: Optional[str] = None
    is_published: bool
    modules: list[CourseModuleRead] = []

    class Config:
        from_attributes = True
