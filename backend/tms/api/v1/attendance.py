from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from tms.api.utils import apply_text_search, paginate, resolve_sort
from tms.auth.security import require_trainer_or_admin
from tms.domain import models, record_audit
from tms.domain.models import AuditActionEnum
from tms.infra.database import get_db
from tms.jobs.queue import enqueue_ssg_sync
from tms.schemas import AttendanceCreate, AttendanceRead, PaginatedResponse, TokenPayload

router = APIRouter()


@router.get(
    "/",
    response_model=PaginatedResponse[AttendanceRead],
    dependencies=[Depends(require_trainer_or_admin)],
)
def list_attendance(
    q: str | None = Query(None, description="Filter by learner or class run reference"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    sort: str | None = Query("-created_at"),
    db: Session = Depends(get_db),
) -> PaginatedResponse[AttendanceRead]:
    query = (
        db.query(models.Attendance)
        .join(models.Attendance.enrollment)
        .join(models.Enrollment.learner)
        .join(models.Enrollment.class_run)
    )
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
            "created_at": models.Attendance.created_at,
            "updated_at": models.Attendance.updated_at,
            "status": models.Attendance.status,
        },
        "-created_at",
    )
    if sort_columns:
        query = query.order_by(*sort_columns)
    items, total = paginate(query, page, page_size)
    return PaginatedResponse[AttendanceRead](
        items=[AttendanceRead.model_validate(entry) for entry in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.post("/", response_model=AttendanceRead, status_code=status.HTTP_201_CREATED)
def create_attendance(
    payload: AttendanceCreate,
    db: Session = Depends(get_db),
    token: TokenPayload = Depends(require_trainer_or_admin),
) -> AttendanceRead:
    enrollment = db.get(models.Enrollment, payload.enrollment_id)
    session = db.get(models.Session, payload.session_id)
    if not enrollment or not session:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Enrollment or session not found")

    attendance = models.Attendance(
        enrollment=enrollment,
        session=session,
        status=models.AttendanceStatusEnum(payload.status),
        remarks=payload.remarks,
    )
    db.add(attendance)
    db.commit()
    db.refresh(attendance)

    record_audit(
        db,
        action=AuditActionEnum.CREATE,
        entity_type="attendance",
        entity_id=str(attendance.id),
        performed_by=uuid.UUID(token.sub),
    )
    db.commit()

    enqueue_ssg_sync("tms.jobs.ssg.sync_attendance_to_ssg", str(attendance.id))
    return AttendanceRead.model_validate(attendance)
