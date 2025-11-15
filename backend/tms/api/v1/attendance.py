from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from tms.auth.security import require_trainer_or_admin
from tms.domain import models, record_audit
from tms.domain.models import AuditActionEnum
from tms.infra.database import get_db
from tms.jobs.queue import enqueue_ssg_sync
from tms.schemas import AttendanceCreate, AttendanceRead, TokenPayload

router = APIRouter()


@router.get("/", response_model=list[AttendanceRead], dependencies=[Depends(require_trainer_or_admin)])
def list_attendance(db: Session = Depends(get_db)) -> list[AttendanceRead]:
    entries = db.query(models.Attendance).all()
    return [AttendanceRead.model_validate(entry) for entry in entries]


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
