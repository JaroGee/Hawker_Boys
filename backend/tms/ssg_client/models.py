from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class SSGTokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


class CoursePayload(BaseModel):
    courseCode: str
    courseTitle: str
    description: Optional[str] = None
    publishFlag: bool = False


class CourseRunPayload(BaseModel):
    courseRunCode: str
    courseCode: str
    startDate: date
    endDate: date
    capacity: int
    location: Optional[str] = None


class LearnerPayload(BaseModel):
    learnerIdentifier: str
    learnerName: str
    contactNumber: Optional[str] = None
    email: Optional[str] = None


class EnrollmentPayload(BaseModel):
    courseRunCode: str
    learnerIdentifier: str
    enrollmentStatus: str


class AttendancePayload(BaseModel):
    courseRunCode: str
    sessionDate: date
    sessionStartTime: datetime
    sessionEndTime: datetime
    learnerIdentifier: str
    attendanceStatus: str


class ClaimPayload(BaseModel):
    courseRunCode: str
    totalClaimAmount: float = Field(ge=0)
    supportingDocumentUrl: Optional[str] = None
