from __future__ import annotations

from typing import TYPE_CHECKING

from tms.ssg_client.models import CoursePayload

if TYPE_CHECKING:  # pragma: no cover - type hints only
    from tms.ssg_client.client import SSGClient


class CourseEndpoint:
    def __init__(self, client: SSGClient) -> None:
        self.client = client

    def create(self, payload: CoursePayload, token: str) -> dict:
        return self.client.create_course(payload, token)

    def update(self, course_id: str, payload: CoursePayload, token: str) -> dict:
        return self.client.update_course(course_id, payload, token)
