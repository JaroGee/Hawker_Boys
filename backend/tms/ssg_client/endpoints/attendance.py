from __future__ import annotations

from typing import TYPE_CHECKING

from loguru import logger

from tms.domain import models
from tms.ssg_client import models as ssg_models

if TYPE_CHECKING:  # pragma: no cover
    from tms.ssg_client.client import SSGClient


class AttendanceEndpoint:
    def __init__(self, client: "SSGClient") -> None:
        self.client = client

    def submit(self, attendance: models.Attendance) -> None:
        payload = ssg_models.SSGAttendancePayload(
            run_id=attendance.session.class_run.ssg_run_id or attendance.session.class_run.reference_code,
            session_date=attendance.session.session_date.isoformat(),
            learner_identifier=attendance.enrollment.learner.masked_nric or str(attendance.enrollment.learner_id),
            status=attendance.status.value,
        )
        # Payload shape informed by ssg-wsg/Sample-Codes examples
        logger.debug("Sending attendance payload to SSG: {}", payload)
        response = self.client.request("POST", "/courses/runs/sessions/attendance", json=payload.__dict__)
        logger.info("Attendance %s synced to SSG with status %s", attendance.id, response.status_code)

