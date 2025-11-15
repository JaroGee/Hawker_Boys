from __future__ import annotations

from tms.ssg_client.client import SSGClient
from tms.ssg_client.models import CourseRunPayload


class ClassRunEndpoint:
    def __init__(self, client: SSGClient) -> None:
        self.client = client

    def create(self, payload: CourseRunPayload, token: str) -> dict:
        return self.client.create_course_run(payload, token)

    def update(self, run_id: str, payload: CourseRunPayload, token: str) -> dict:
        return self.client.update_course_run(run_id, payload, token)
