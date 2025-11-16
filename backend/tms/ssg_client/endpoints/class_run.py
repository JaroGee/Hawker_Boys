from __future__ import annotations

from typing import TYPE_CHECKING

from tms.ssg_client.models import CourseRunPayload

if TYPE_CHECKING:  # pragma: no cover
    from tms.ssg_client.client import SSGClient


class ClassRunEndpoint:
    def __init__(self, client: SSGClient) -> None:
        self.client = client

    def create(self, payload: CourseRunPayload, token: str) -> dict:
        return self.client.create_course_run(payload, token)

    def update(self, run_id: str, payload: CourseRunPayload, token: str) -> dict:
        return self.client.update_course_run(run_id, payload, token)
