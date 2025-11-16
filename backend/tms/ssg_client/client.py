from __future__ import annotations

import datetime as dt
from typing import Any

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from tms.infra.config import settings
from tms.ssg_client import models
from tms.ssg_client.endpoints import courses, class_runs, attendance


class SSGClientError(Exception):
    """Raised when the SSG API returns an error."""


class SSGClient:
    """Minimal SSG API client inspired by official Sample-Codes repo."""

    def __init__(self, base_url: str, client_id: str, client_secret: str, timeout: int) -> None:
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.timeout = timeout
        self._token: models.SSGAuthToken | None = None
        self._http = httpx.Client(base_url=self.base_url, timeout=self.timeout)
        self.courses = courses.CourseEndpoint(self)
        self.class_runs = class_runs.ClassRunEndpoint(self)
        self.attendance = attendance.AttendanceEndpoint(self)

    @classmethod
    def from_settings(cls) -> "SSGClient":
        return cls(
            base_url=settings.ssg_base_url,
            client_id=settings.ssg_client_id,
            client_secret=settings.ssg_client_secret,
            timeout=settings.ssg_timeout_seconds,
        )

    @retry(wait=wait_exponential(multiplier=1, min=1, max=10), stop=stop_after_attempt(3))
    def _authenticate(self) -> models.SSGAuthToken:
        if self._token and self._token.expires_in > int(dt.datetime.utcnow().timestamp()):
            return self._token

        # Based on oauth2 pattern shown in ssg-wsg/Sample-Codes repo
        response = self._http.post(
            "/oauth2/token",
            data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "client_credentials",
            },
        )
        response.raise_for_status()
        payload = response.json()
        token = models.SSGAuthToken(
            access_token=payload["access_token"],
            token_type=payload.get("token_type", "Bearer"),
            expires_in=int(dt.datetime.utcnow().timestamp()) + int(payload.get("expires_in", 3600)),
        )
        self._token = token
        return token

    def _headers(self) -> dict[str, str]:
        token = self._authenticate()
        return {
            "Authorization": f"Bearer {token.access_token}",
            "Content-Type": "application/json",
            "X-SSG-Env": settings.ssg_env,
        }

    def request(self, method: str, path: str, *, json: Any | None = None) -> httpx.Response:
        response = self._http.request(method, path, headers=self._headers(), json=json)
        if response.status_code >= 400:
            self._handle_error(response)
        return response

    def _handle_error(self, response: httpx.Response) -> None:
        detail = response.json() if response.content else {}
        raise httpx.HTTPStatusError(
            f"SSG API error {response.status_code}", request=response.request, response=response
        )
