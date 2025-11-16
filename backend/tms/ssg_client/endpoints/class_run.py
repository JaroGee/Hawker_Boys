from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # pragma: no cover
    from tms.ssg_client.client import SSGClient


class ClassRunEndpoint:
    def __init__(self, client: SSGClient) -> None:
        self.client = client

    def create(self, payload: Any, token: str) -> dict:
        return self.client.create_course_run(payload, token)

    def update(self, run_id: str, payload: Any, token: str) -> dict:
        return self.client.update_course_run(run_id, payload, token)
