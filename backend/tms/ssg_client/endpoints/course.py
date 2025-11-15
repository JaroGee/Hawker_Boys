from __future__ import annotations

from tms.ssg_client.client import SSGClient
from tms.ssg_client.models import CoursePayload


class CourseEndpoint:
    def __init__(self, client: SSGClient) -> None:
        self.client = client

    def create(self, payload: CoursePayload, token: str) -> dict:
        return self.client.create_course(payload, token)

    def update(self, course_id: str, payload: CoursePayload, token: str) -> dict:
        return self.client.update_course(course_id, payload, token)
