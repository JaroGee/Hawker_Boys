from __future__ import annotations

from typing import TYPE_CHECKING

from loguru import logger

from tms.domain import models
from tms.ssg_client import models as ssg_models

if TYPE_CHECKING:  # pragma: no cover
    from tms.ssg_client.client import SSGClient


class ClassRunEndpoint:
    def __init__(self, client: "SSGClient") -> None:
        self.client = client

    def create_or_update(self, class_run: models.ClassRun) -> None:
        payload = ssg_models.SSGClassRunPayload(
            course_code=class_run.course.code,
            run_id=class_run.ssg_run_id,
            reference_code=class_run.reference_code,
            start_date=class_run.start_date.isoformat(),
            end_date=class_run.end_date.isoformat(),
            status=class_run.status.value,
        )
        # Payload shape informed by ssg-wsg/Sample-Codes examples
        logger.debug("Sending class run payload to SSG: {}", payload)
        response = self.client.request("POST", "/courses/courseRuns", json=payload.__dict__)
        logger.info("Class run %s synced to SSG with status %s", class_run.id, response.status_code)


from tms.ssg_client.client import SSGClient  # noqa: E402 circular import guard
