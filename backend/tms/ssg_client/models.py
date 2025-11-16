from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class SSGAuthToken:
    access_token: str
    token_type: str
    expires_in: int


@dataclass
class SSGError:
    code: str
    message: str
    details: Any | None = None


@dataclass
class SSGCoursePayload:
    course_code: str
    title: str
    description: str | None
    status: str


@dataclass
class SSGClassRunPayload:
    course_code: str
    run_id: str | None
    reference_code: str
    start_date: str
    end_date: str
    status: str


@dataclass
class SSGAttendancePayload:
    run_id: str
    session_date: str
    learner_identifier: str
    status: str


# Legacy payload aliases for the queue module. Keeping them lightweight avoids
# import errors during tests even though the real SSG contract lives elsewhere.
@dataclass
class CoursePayload:
    courseCode: str
    courseTitle: str
    description: str | None
    publishFlag: bool


@dataclass
class CourseRunPayload:
    courseRunCode: str
    courseCode: str
    startDate: str
    endDate: str
    capacity: int | None = None
    location: str | None = None


@dataclass
class EnrollmentPayload:
    courseRunCode: str
    learnerIdentifier: str
    enrollmentStatus: str


@dataclass
class AttendancePayload:
    courseRunCode: str
    sessionDate: str
    sessionStartTime: str | None
    sessionEndTime: str | None
    learnerIdentifier: str
    attendanceStatus: str


@dataclass
class ClaimPayload:
    reference_id: str
    amount: float
    metadata: Any | None = None
