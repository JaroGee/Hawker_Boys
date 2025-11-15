from __future__ import annotations

from loguru import logger

from tms.domain import models
from tms.ssg_client import models as ssg_models


class CourseEndpoint:
    def __init__(self, client: "SSGClient") -> None:
        self.client = client

    def create_or_update(self, course: models.Course) -> None:
        payload = ssg_models.SSGCoursePayload(
            course_code=course.code,
            title=course.title,
            description=course.description,
            status="active" if course.is_active else "inactive",
        )
        # Payload shape informed by ssg-wsg/Sample-Codes examples
        logger.debug("Sending course payload to SSG: {}", payload)
        response = self.client.request("POST", "/courses", json=payload.__dict__)
        logger.info("Course %s synced to SSG with status %s", course.id, response.status_code)


from tms.ssg_client.client import SSGClient  # noqa: E402 circular import guard
