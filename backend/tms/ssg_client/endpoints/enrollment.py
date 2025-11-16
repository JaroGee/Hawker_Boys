from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # pragma: no cover
    from tms.ssg_client.client import SSGClient


class EnrollmentEndpoint:
    def __init__(self, client: SSGClient) -> None:
        self.client = client

    def submit_enrollment(self, payload: Any, token: str) -> dict:
        return self.client.submit_enrollment(payload, token)

    def submit_attendance(self, payload: Any, token: str) -> dict:
        return self.client.submit_attendance(payload, token)
