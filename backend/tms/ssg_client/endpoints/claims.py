from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # pragma: no cover
    from tms.ssg_client.client import SSGClient


class ClaimsEndpoint:
    def __init__(self, client: SSGClient) -> None:
        self.client = client

    def submit(self, payload: Any, token: str) -> dict:
        return self.client.submit_claim(payload, token)
