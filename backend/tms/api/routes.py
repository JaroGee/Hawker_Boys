from __future__ import annotations

from fastapi import APIRouter

from tms.api.v1 import auth, courses, learners, enrollments, attendance, assessments, certificates, audit

api_router = APIRouter(prefix="/api")
api_router.include_router(auth.router, prefix="/v1/auth", tags=["auth"])
api_router.include_router(courses.router, prefix="/v1/courses", tags=["courses"])
api_router.include_router(learners.router, prefix="/v1/learners", tags=["learners"])
api_router.include_router(enrollments.router, prefix="/v1/enrollments", tags=["enrollments"])
api_router.include_router(attendance.router, prefix="/v1/attendance", tags=["attendance"])
api_router.include_router(assessments.router, prefix="/v1/assessments", tags=["assessments"])
api_router.include_router(certificates.router, prefix="/v1/certificates", tags=["certificates"])
api_router.include_router(audit.router, prefix="/v1/audit", tags=["audit"])
