from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from tms.api.dependencies import get_db, require_role
from tms.auth.authz import Role
from tms.domain.models import Course, CourseModule
from tms.domain.services import queue_course_sync
from tms.schemas import CourseCreate, CourseRead, CourseUpdate

router = APIRouter(prefix="/courses")


@router.post("", response_model=CourseRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_role(Role.OPS, Role.ADMIN))])
def create_course(payload: CourseCreate, db: Session = Depends(get_db)) -> CourseRead:
    existing = db.query(Course).filter_by(code=payload.code).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Course code already exists.")
    course = Course(code=payload.code, title=payload.title, description=payload.description)
    for module in payload.modules:
        course.modules.append(
            CourseModule(
                code=module.code,
                title=module.title,
                description=module.description,
                duration_hours=module.duration_hours,
            )
        )
    db.add(course)
    db.commit()
    db.refresh(course)
    queue_course_sync(course)
    return CourseRead.model_validate(course)


@router.get("", response_model=list[CourseRead], dependencies=[Depends(require_role(Role.OPS, Role.TRAINER, Role.ADMIN))])
def list_courses(db: Session = Depends(get_db)) -> list[CourseRead]:
    courses = db.query(Course).all()
    return [CourseRead.model_validate(c) for c in courses]


@router.get("/{course_id}", response_model=CourseRead, dependencies=[Depends(require_role(Role.OPS, Role.TRAINER, Role.ADMIN))])
def get_course(course_id: str, db: Session = Depends(get_db)) -> CourseRead:
    course = db.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found.")
    return CourseRead.model_validate(course)


@router.patch("/{course_id}", response_model=CourseRead, dependencies=[Depends(require_role(Role.OPS, Role.ADMIN))])
def update_course(course_id: str, payload: CourseUpdate, db: Session = Depends(get_db)) -> CourseRead:
    course = db.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found.")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(course, field, value)
    db.add(course)
    db.commit()
    db.refresh(course)
    queue_course_sync(course)
    return CourseRead.model_validate(course)


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_role(Role.ADMIN))])
def delete_course(course_id: str, db: Session = Depends(get_db)) -> None:
    course = db.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found.")
    db.delete(course)
    db.commit()
