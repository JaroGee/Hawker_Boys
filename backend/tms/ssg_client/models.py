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
