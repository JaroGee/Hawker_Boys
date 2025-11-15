from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from tms.api.dependencies import get_db, require_role
from tms.auth.authz import Role
from tms.domain.models import ClassRun, Course, Session as SessionModel
from tms.domain.services import queue_class_run_sync
from tms.schemas import ClassRunCreate, ClassRunRead, ClassRunUpdate

router = APIRouter(prefix="/class-runs")


@router.post("", response_model=ClassRunRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_role(Role.OPS, Role.ADMIN))])
def create_class_run(payload: ClassRunCreate, db: Session = Depends(get_db)) -> ClassRunRead:
    course = db.get(Course, payload.course_id)
    if not course:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Course not found.")
    existing = db.query(ClassRun).filter_by(code=payload.code).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Class run code already exists.")
    class_run = ClassRun(
        course_id=payload.course_id,
        code=payload.code,
        start_date=payload.start_date,
        end_date=payload.end_date,
        capacity=payload.capacity,
        location=payload.location,
    )
    for session in payload.sessions:
        class_run.sessions.append(
            SessionModel(
                module_id=session.module_id,
                session_date=session.session_date,
                start_time=session.start_time,
                end_time=session.end_time,
            )
        )
    db.add(class_run)
    db.commit()
    db.refresh(class_run)
    queue_class_run_sync(class_run)
    return ClassRunRead.model_validate(class_run)


@router.get("", response_model=list[ClassRunRead], dependencies=[Depends(require_role(Role.OPS, Role.TRAINER, Role.ADMIN))])
def list_class_runs(db: Session = Depends(get_db)) -> list[ClassRunRead]:
    runs = db.query(ClassRun).all()
    return [ClassRunRead.model_validate(run) for run in runs]


@router.get("/{class_run_id}", response_model=ClassRunRead, dependencies=[Depends(require_role(Role.OPS, Role.TRAINER, Role.ADMIN))])
def get_class_run(class_run_id: str, db: Session = Depends(get_db)) -> ClassRunRead:
    class_run = db.get(ClassRun, class_run_id)
    if not class_run:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Class run not found.")
    return ClassRunRead.model_validate(class_run)


@router.patch("/{class_run_id}", response_model=ClassRunRead, dependencies=[Depends(require_role(Role.OPS, Role.ADMIN))])
def update_class_run(class_run_id: str, payload: ClassRunUpdate, db: Session = Depends(get_db)) -> ClassRunRead:
    class_run = db.get(ClassRun, class_run_id)
    if not class_run:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Class run not found.")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(class_run, field, value)
    db.add(class_run)
    db.commit()
    db.refresh(class_run)
    queue_class_run_sync(class_run)
    return ClassRunRead.model_validate(class_run)
