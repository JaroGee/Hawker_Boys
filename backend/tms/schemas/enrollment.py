from __future__ import annotations

import uuid
from typing import Optional

from pydantic import BaseModel

from tms.domain.models import AttendanceStatus, EnrollmentStatus


class EnrollmentCreate(BaseModel):
    learner_id: uuid.UUID
    class_run_id: uuid.UUID


class EnrollmentUpdate(BaseModel):
    status: Optional[EnrollmentStatus] = None
    ssg_enrollment_id: Optional[str] = None


class EnrollmentRead(BaseModel):
    id: uuid.UUID
    learner_id: uuid.UUID
    class_run_id: uuid.UUID
    status: EnrollmentStatus
    ssg_enrollment_id: Optional[str]

    class Config:
        from_attributes = True


class AttendanceCreate(BaseModel):
    enrollment_id: uuid.UUID
    session_id: uuid.UUID
    status: AttendanceStatus
    remarks: Optional[str] = None


class AttendanceRead(BaseModel):
    id: uuid.UUID
    enrollment_id: uuid.UUID
    session_id: uuid.UUID
    status: AttendanceStatus
    remarks: Optional[str]

    class Config:
        from_attributes = True
