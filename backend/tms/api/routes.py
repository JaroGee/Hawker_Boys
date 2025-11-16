from __future__ import annotations

from fastapi import APIRouter

from tms.api.v1 import (
    auth,
    attendance,
    assessments,
    audit,
    certificates,
    class_runs,
    courses,
    enrollments,
    learners,
    ssg,
)

api_router = APIRouter(prefix="/api")
api_router.include_router(auth.router, prefix="/v1/auth", tags=["auth"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(courses.router, prefix="/v1/courses", tags=["courses"])
api_router.include_router(learners.router, prefix="/v1/learners", tags=["learners"])
api_router.include_router(enrollments.router, prefix="/v1/enrollments", tags=["enrollments"])
api_router.include_router(attendance.router, prefix="/v1/attendance", tags=["attendance"])
api_router.include_router(assessments.router, prefix="/v1/assessments", tags=["assessments"])
api_router.include_router(certificates.router, prefix="/v1/certificates", tags=["certificates"])
api_router.include_router(audit.router, prefix="/v1/audit", tags=["audit"])
api_router.include_router(class_runs.router, prefix="/v1/class-runs", tags=["class_runs"])
api_router.include_router(ssg.router, prefix="/ssg", tags=["ssg"])
