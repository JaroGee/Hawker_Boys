from __future__ import annotations

from tms.domain.models import Attendance, ClassRun, Course, Enrollment
from tms.infra.database import SessionLocal
from tms.infra.logging import get_logger
from tms.ssg_client.client import SSGClient
from tms.ssg_client.models import AttendancePayload, CoursePayload, CourseRunPayload, EnrollmentPayload

logger = get_logger(__name__)
# Sync payload shapes follow SSG Sample-Codes guidance: https://github.com/ssg-wsg/Sample-Codes


def _get_token(client: SSGClient) -> str:
    return client.obtain_token().access_token


def sync_course(course_id: str) -> None:
    logger.info("sync_course_start", course_id=course_id)
    with SessionLocal() as db:
        course = db.get(Course, course_id)
        if not course:
            logger.warning("sync_course_missing", course_id=course_id)
            return
        client = SSGClient()
        token = _get_token(client)
        payload = CoursePayload(courseCode=course.code, courseTitle=course.title, description=course.description, publishFlag=course.is_published)
        client.create_course(payload, token)
    logger.info("sync_course_complete", course_id=course_id)


def sync_class_run(class_run_id: str) -> None:
    logger.info("sync_class_run_start", class_run_id=class_run_id)
    with SessionLocal() as db:
        run = db.get(ClassRun, class_run_id)
        if not run:
            logger.warning("sync_class_run_missing", class_run_id=class_run_id)
            return
        client = SSGClient()
        token = _get_token(client)
        payload = CourseRunPayload(
            courseRunCode=run.code,
            courseCode=run.course.code,
            startDate=run.start_date,
            endDate=run.end_date,
            capacity=run.capacity,
            location=run.location,
        )
        client.create_course_run(payload, token)
    logger.info("sync_class_run_complete", class_run_id=class_run_id)


def sync_enrollment(enrollment_id: str) -> None:
    logger.info("sync_enrollment_start", enrollment_id=enrollment_id)
    with SessionLocal() as db:
        enrollment = db.get(Enrollment, enrollment_id)
        if not enrollment:
            logger.warning("sync_enrollment_missing", enrollment_id=enrollment_id)
            return
        client = SSGClient()
        token = _get_token(client)
        payload = EnrollmentPayload(
            courseRunCode=enrollment.class_run.code,
            learnerIdentifier=enrollment.learner.hashed_identifier or str(enrollment.learner_id),
            enrollmentStatus=enrollment.status.value,
        )
        client.submit_enrollment(payload, token)
    logger.info("sync_enrollment_complete", enrollment_id=enrollment_id)


def sync_attendance(attendance_id: str) -> None:
    logger.info("sync_attendance_start", attendance_id=attendance_id)
    with SessionLocal() as db:
        attendance = db.get(Attendance, attendance_id)
        if not attendance:
            logger.warning("sync_attendance_missing", attendance_id=attendance_id)
            return
        client = SSGClient()
        token = _get_token(client)
        session = attendance.session
        payload = AttendancePayload(
            courseRunCode=attendance.enrollment.class_run.code,
            sessionDate=session.session_date,
            sessionStartTime=session.start_time,
            sessionEndTime=session.end_time,
            learnerIdentifier=attendance.enrollment.learner.hashed_identifier or str(attendance.enrollment.learner_id),
            attendanceStatus=attendance.status.value,
        )
        client.submit_attendance(payload, token)
    logger.info("sync_attendance_complete", attendance_id=attendance_id)
