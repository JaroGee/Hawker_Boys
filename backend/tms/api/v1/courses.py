from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from tms.api.utils import apply_text_search, paginate, resolve_sort
from tms.auth.security import require_ops_or_admin
from tms.domain import models, record_audit
from tms.domain.models import AuditActionEnum
from tms.infra.database import get_db
from tms.jobs.queue import enqueue_ssg_sync
from tms.schemas import (
    CourseCreate,
    CourseRead,
    CourseUpdate,
    ClassRunCreate,
    ClassRunRead,
    PaginatedResponse,
    TokenPayload,
)

router = APIRouter()


@router.get(
    "/",
    response_model=PaginatedResponse[CourseRead],
    dependencies=[Depends(require_ops_or_admin)],
)
def list_courses(
    q: str | None = Query(None, description="Filter by code or title"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    sort: str | None = Query("-created_at"),
    db: Session = Depends(get_db),
) -> PaginatedResponse[CourseRead]:
    query = db.query(models.Course)
    query = apply_text_search(query, [models.Course.code, models.Course.title], q)
    sort_columns = resolve_sort(
        sort,
        {
            "code": models.Course.code,
            "title": models.Course.title,
            "created_at": models.Course.created_at,
            "updated_at": models.Course.updated_at,
        },
        "-created_at",
    )
    if sort_columns:
        query = query.order_by(*sort_columns)
    items, total = paginate(query, page, page_size)
    payload = [CourseRead.model_validate(course) for course in items]
    return PaginatedResponse[CourseRead](items=payload, total=total, page=page, page_size=page_size)


@router.get("/{course_id}", response_model=CourseRead, dependencies=[Depends(require_ops_or_admin)])
def get_course(course_id: uuid.UUID, db: Session = Depends(get_db)) -> CourseRead:
    course = db.get(models.Course, course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return CourseRead.model_validate(course)


@router.post("/", response_model=CourseRead, status_code=status.HTTP_201_CREATED)
def create_course(
    course: CourseCreate,
    db: Session = Depends(get_db),
    token: TokenPayload = Depends(require_ops_or_admin),
) -> CourseRead:
    if db.query(models.Course).filter_by(code=course.code).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Course code already exists")

    db_course = models.Course(code=course.code, title=course.title, description=course.description)
    for module in course.modules:
        db_course.modules.append(models.Module(title=module.title, description=module.description, order=module.order))

    db.add(db_course)
    db.commit()
    db.refresh(db_course)

    record_audit(
        db,
        action=AuditActionEnum.CREATE,
        entity_type="course",
        entity_id=str(db_course.id),
        performed_by=uuid.UUID(token.sub),
    )
    db.commit()

    enqueue_ssg_sync("tms.jobs.ssg.sync_course_to_ssg", str(db_course.id))
    return CourseRead.model_validate(db_course)


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(
    course_id: uuid.UUID,
    db: Session = Depends(get_db),
    token: TokenPayload = Depends(require_ops_or_admin),
) -> None:
    course = db.get(models.Course, course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    db.delete(course)
    record_audit(
        db,
        action=AuditActionEnum.DELETE,
        entity_type="course",
        entity_id=str(course.id),
        performed_by=uuid.UUID(token.sub),
    )
    db.commit()
@router.patch("/{course_id}", response_model=CourseRead)
def update_course(
    course_id: uuid.UUID,
    payload: CourseUpdate,
    db: Session = Depends(get_db),
    token: TokenPayload = Depends(require_ops_or_admin),
) -> CourseRead:
    db_course = db.get(models.Course, course_id)
    if not db_course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(db_course, field, value)

    db.commit()
    db.refresh(db_course)

    record_audit(
        db,
        action=AuditActionEnum.UPDATE,
        entity_type="course",
        entity_id=str(db_course.id),
        performed_by=uuid.UUID(token.sub),
    )
    db.commit()

    enqueue_ssg_sync("tms.jobs.ssg.sync_course_to_ssg", str(db_course.id))
    return CourseRead.model_validate(db_course)


@router.post("/{course_id}/runs", response_model=ClassRunRead, status_code=status.HTTP_201_CREATED)
def create_class_run(
    course_id: uuid.UUID,
    payload: ClassRunCreate,
    db: Session = Depends(get_db),
    token: TokenPayload = Depends(require_ops_or_admin),
) -> ClassRunRead:
    course = db.get(models.Course, course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    class_run = models.ClassRun(
        course=course,
        reference_code=payload.reference_code,
        start_date=payload.start_date,
        end_date=payload.end_date,
        status=models.ClassRunStatusEnum(payload.status),
    )
    db.add(class_run)
    db.commit()
    db.refresh(class_run)

    record_audit(
        db,
        action=AuditActionEnum.CREATE,
        entity_type="class_run",
        entity_id=str(class_run.id),
        performed_by=uuid.UUID(token.sub),
    )
    db.commit()

    enqueue_ssg_sync("tms.jobs.ssg.sync_class_run_to_ssg", str(class_run.id))
    return ClassRunRead.model_validate(class_run)
