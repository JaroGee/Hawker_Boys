from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from tms.api.dependencies import get_db, require_role
from tms.auth.authz import Role
from tms.domain.models import Attendance, Enrollment, Session as SessionModel
from tms.domain.services import queue_attendance_sync
from tms.schemas import AttendanceCreate, AttendanceRead

router = APIRouter(prefix="/attendance")


@router.post("", response_model=AttendanceRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_role(Role.OPS, Role.TRAINER, Role.ADMIN))])
def create_attendance(payload: AttendanceCreate, db: Session = Depends(get_db)) -> AttendanceRead:
    enrollment = db.get(Enrollment, payload.enrollment_id)
    session_model = db.get(SessionModel, payload.session_id)
    if not enrollment or not session_model:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Enrollment or session not found.")
    existing = (
        db.query(Attendance)
        .filter(Attendance.enrollment_id == payload.enrollment_id, Attendance.session_id == payload.session_id)
        .first()
    )
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Attendance already recorded.")
    attendance = Attendance(
        enrollment_id=payload.enrollment_id,
        session_id=payload.session_id,
        status=payload.status,
        remarks=payload.remarks,
    )
    db.add(attendance)
    db.commit()
    db.refresh(attendance)
    queue_attendance_sync(attendance)
    return AttendanceRead.model_validate(attendance)


@router.get("", response_model=list[AttendanceRead], dependencies=[Depends(require_role(Role.OPS, Role.TRAINER, Role.ADMIN))])
def list_attendance(db: Session = Depends(get_db)) -> list[AttendanceRead]:
    records = db.query(Attendance).all()
    return [AttendanceRead.model_validate(record) for record in records]
