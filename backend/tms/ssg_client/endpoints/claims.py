from __future__ import annotations

from tms.ssg_client.client import SSGClient
from tms.ssg_client.models import ClaimPayload


class ClaimsEndpoint:
    def __init__(self, client: SSGClient) -> None:
        self.client = client

    def submit(self, payload: ClaimPayload, token: str) -> dict:
        return self.client.submit_claim(payload, token)
