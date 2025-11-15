from __future__ import annotations

from fastapi import APIRouter, FastAPI

from tms.api.routes import courses, class_runs, learners, enrollments, attendance


def register_routes(app: FastAPI) -> None:
    api_router = APIRouter(prefix="/api/v1")
    api_router.include_router(courses.router, tags=["courses"])
    api_router.include_router(class_runs.router, tags=["class_runs"])
    api_router.include_router(learners.router, tags=["learners"])
    api_router.include_router(enrollments.router, tags=["enrollments"])
    api_router.include_router(attendance.router, tags=["attendance"])
    app.include_router(api_router)
