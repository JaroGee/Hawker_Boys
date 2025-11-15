from __future__ import annotations

import uuid
from typing import Any, Callable, Optional

import httpx
from tenacity import RetryError, retry, stop_after_attempt, wait_exponential

from tms.infra.logging import get_logger
from tms.settings import settings

# Payload structures adapted from https://github.com/ssg-wsg/Sample-Codes for Training Provider flows
from .models import (
    AttendancePayload,
    ClaimPayload,
    CoursePayload,
    CourseRunPayload,
    EnrollmentPayload,
    SSGTokenResponse,
)

logger = get_logger(__name__)


class SSGClientError(Exception):
    def __init__(self, message: str, *, status_code: int | None = None, payload: Any | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.payload = payload


class SSGClient:
    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = base_url or settings.ssg_base_url.rstrip("/")
        self.timeout = settings.ssg_timeout_seconds
        self.client_id = settings.ssg_client_id
        self.client_secret = settings.ssg_client_secret
        self._client = httpx.Client(timeout=self.timeout)

    def _headers(self, token: str | None = None) -> dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "X-Env": settings.ssg_env,
            "X-Correlation-ID": str(uuid.uuid4()),
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers

    def _request(self, method: str, path: str, *, token: str | None = None, json: Any | None = None) -> httpx.Response:
        url = f"{self.base_url}{path}"
        logger.info("ssg_request", method=method, url=url, has_payload=json is not None)
        response = self._client.request(method, url, headers=self._headers(token), json=json)
        if response.status_code >= 400:
            logger.error("ssg_error", status=response.status_code, body=response.text)
            raise SSGClientError("SSG request failed", status_code=response.status_code, payload=response.text)
        return response

    def obtain_token(self) -> SSGTokenResponse:
        response = self._client.post(
            f"{self.base_url}/oauth/token",
            data={"client_id": self.client_id, "client_secret": self.client_secret, "grant_type": "client_credentials"},
        )
        if response.status_code >= 400:
            logger.error("ssg_token_error", status=response.status_code, body=response.text)
            raise SSGClientError("Failed to obtain SSG access token", status_code=response.status_code, payload=response.text)
        return SSGTokenResponse.model_validate(response.json())

    def _with_retry(self, func: Callable[[], httpx.Response]) -> httpx.Response:
        @retry(wait=wait_exponential(multiplier=1, min=1, max=10), stop=stop_after_attempt(3))
        def inner() -> httpx.Response:
            return func()

        try:
            return inner()
        except RetryError as exc:
            raise SSGClientError("SSG request failed after retries") from exc

    def create_course(self, payload: CoursePayload, token: str) -> dict[str, Any]:
        response = self._with_retry(lambda: self._request("POST", "/courses", token=token, json=payload.model_dump(by_alias=True)))
        return response.json()

    def update_course(self, course_id: str, payload: CoursePayload, token: str) -> dict[str, Any]:
        response = self._with_retry(
            lambda: self._request("PUT", f"/courses/{course_id}", token=token, json=payload.model_dump(by_alias=True))
        )
        return response.json()

    def create_course_run(self, payload: CourseRunPayload, token: str) -> dict[str, Any]:
        response = self._with_retry(
            lambda: self._request("POST", "/courses/courseRuns", token=token, json=payload.model_dump(by_alias=True))
        )
        return response.json()

    def update_course_run(self, run_id: str, payload: CourseRunPayload, token: str) -> dict[str, Any]:
        response = self._with_retry(
            lambda: self._request(
                "PUT",
                f"/courses/courseRuns/{run_id}",
                token=token,
                json=payload.model_dump(by_alias=True),
            )
        )
        return response.json()

    def submit_enrollment(self, payload: EnrollmentPayload, token: str) -> dict[str, Any]:
        response = self._with_retry(
            lambda: self._request(
                "POST",
                "/courses/courseRuns/enrolments",
                token=token,
                json=payload.model_dump(by_alias=True),
            )
        )
        return response.json()

    def submit_attendance(self, payload: AttendancePayload, token: str) -> dict[str, Any]:
        response = self._with_retry(
            lambda: self._request(
                "POST",
                "/courses/courseRuns/sessions/attendance",
                token=token,
                json=payload.model_dump(by_alias=True),
            )
        )
        return response.json()

    def submit_claim(self, payload: ClaimPayload, token: str) -> dict[str, Any]:
        response = self._with_retry(
            lambda: self._request("POST", "/courses/courseRuns/claims", token=token, json=payload.model_dump(by_alias=True))
        )
        return response.json()
