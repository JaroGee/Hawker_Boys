from __future__ import annotations

from tms.ssg_client.client import SSGClient
from tms.ssg_client.models import AttendancePayload, EnrollmentPayload


class EnrollmentEndpoint:
    def __init__(self, client: SSGClient) -> None:
        self.client = client

    def submit_enrollment(self, payload: EnrollmentPayload, token: str) -> dict:
        return self.client.submit_enrollment(payload, token)

    def submit_attendance(self, payload: AttendancePayload, token: str) -> dict:
        return self.client.submit_attendance(payload, token)
