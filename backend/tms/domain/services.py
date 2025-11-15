from __future__ import annotations

from tms.domain.models import Attendance, ClassRun, Course, Enrollment
from tms.jobs.queue import get_job_queue
from tms.jobs import ssg_sync


def queue_course_sync(course: Course) -> None:
    get_job_queue().enqueue(ssg_sync.sync_course, str(course.id))


def queue_class_run_sync(class_run: ClassRun) -> None:
    get_job_queue().enqueue(ssg_sync.sync_class_run, str(class_run.id))


def queue_enrollment_sync(enrollment: Enrollment) -> None:
    get_job_queue().enqueue(ssg_sync.sync_enrollment, str(enrollment.id))


def queue_attendance_sync(attendance: Attendance) -> None:
    get_job_queue().enqueue(ssg_sync.sync_attendance, str(attendance.id))
