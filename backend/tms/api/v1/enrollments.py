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
    EnrollmentCreate,
    EnrollmentRead,
    EnrollmentUpdate,
    PaginatedResponse,
    TokenPayload,
)

router = APIRouter()


@router.get(
    "/",
    response_model=PaginatedResponse[EnrollmentRead],
    dependencies=[Depends(require_ops_or_admin)],
)
def list_enrollments(
    q: str | None = Query(None, description="Filter by learner or class run"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    sort: str | None = Query("-created_at"),
    db: Session = Depends(get_db),
) -> PaginatedResponse[EnrollmentRead]:
    query = db.query(models.Enrollment).join(models.Learner).join(models.ClassRun)
    query = apply_text_search(
        query,
        [
            models.Learner.given_name,
            models.Learner.family_name,
            models.ClassRun.reference_code,
        ],
        q,
    )
    sort_columns = resolve_sort(
        sort,
        {
            "created_at": models.Enrollment.created_at,
            "enrollment_date": models.Enrollment.enrollment_date,
            "status": models.Enrollment.status,
        },
        "-created_at",
    )
    if sort_columns:
        query = query.order_by(*sort_columns)
    items, total = paginate(query, page, page_size)
    return PaginatedResponse[EnrollmentRead](
        items=[EnrollmentRead.model_validate(enrollment) for enrollment in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.post("/", response_model=EnrollmentRead, status_code=status.HTTP_201_CREATED)
def create_enrollment(
    payload: EnrollmentCreate,
    db: Session = Depends(get_db),
    token: TokenPayload = Depends(require_ops_or_admin),
) -> EnrollmentRead:
    learner = db.get(models.Learner, payload.learner_id)
    class_run = db.get(models.ClassRun, payload.class_run_id)
    if not learner or not class_run:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Learner or class run not found")

    if db.query(models.Enrollment).filter_by(learner_id=learner.id, class_run_id=class_run.id).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Learner already enrolled")

    enrollment = models.Enrollment(
        learner=learner,
        class_run=class_run,
        status=models.EnrollmentStatusEnum(payload.status),
    )
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)

    record_audit(
        db,
        action=AuditActionEnum.CREATE,
        entity_type="enrollment",
        entity_id=str(enrollment.id),
        performed_by=uuid.UUID(token.sub),
    )
    db.commit()

    enqueue_ssg_sync("tms.jobs.ssg.sync_class_run_to_ssg", str(class_run.id))
    return EnrollmentRead.model_validate(enrollment)


@router.patch("/{enrollment_id}", response_model=EnrollmentRead)
def update_enrollment(
    enrollment_id: uuid.UUID,
    payload: EnrollmentUpdate,
    db: Session = Depends(get_db),
    token: TokenPayload = Depends(require_ops_or_admin),
) -> EnrollmentRead:
    enrollment = db.get(models.Enrollment, enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enrollment not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        if field == "status" and value is not None:
            setattr(enrollment, field, models.EnrollmentStatusEnum(value))
        elif value is not None:
            setattr(enrollment, field, value)

    db.commit()
    db.refresh(enrollment)

    record_audit(
        db,
        action=AuditActionEnum.UPDATE,
        entity_type="enrollment",
        entity_id=str(enrollment.id),
        performed_by=uuid.UUID(token.sub),
    )
    db.commit()

    enqueue_ssg_sync("tms.jobs.ssg.sync_class_run_to_ssg", str(enrollment.class_run_id))
    return EnrollmentRead.model_validate(enrollment)
