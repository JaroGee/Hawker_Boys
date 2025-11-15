from __future__ import annotations

from loguru import logger
from sqlalchemy.orm import Session

from tms.domain import models
from tms.infra.database import session_scope
from tms.ssg_client.client import SSGClient


def sync_course_to_ssg(course_id: str) -> None:
    logger.info("Syncing course {} to SSG", course_id)
    with session_scope() as session:
        course = session.get(models.Course, course_id)
        if not course:
            logger.warning("Course %s not found for SSG sync", course_id)
            return
        client = SSGClient.from_settings()
        client.courses.create_or_update(course)


def sync_class_run_to_ssg(class_run_id: str) -> None:
    logger.info("Syncing class run {} to SSG", class_run_id)
    with session_scope() as session:
        class_run = session.get(models.ClassRun, class_run_id)
        if not class_run:
            logger.warning("Class run %s not found for SSG sync", class_run_id)
            return
        client = SSGClient.from_settings()
        client.class_runs.create_or_update(class_run)


def sync_attendance_to_ssg(attendance_id: str) -> None:
    logger.info("Syncing attendance {} to SSG", attendance_id)
    with session_scope() as session:
        attendance = session.get(models.Attendance, attendance_id)
        if not attendance:
            logger.warning("Attendance %s not found for SSG sync", attendance_id)
            return
        client = SSGClient.from_settings()
        client.attendance.submit(attendance)
