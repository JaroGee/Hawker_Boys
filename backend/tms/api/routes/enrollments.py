from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from tms.api.dependencies import get_db, require_role
from tms.auth.authz import Role
from tms.domain.models import ClassRun, Enrollment, Learner
from tms.domain.services import queue_enrollment_sync
from tms.schemas import EnrollmentCreate, EnrollmentRead, EnrollmentUpdate

router = APIRouter(prefix="/enrollments")


@router.post("", response_model=EnrollmentRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_role(Role.OPS, Role.ADMIN))])
def create_enrollment(payload: EnrollmentCreate, db: Session = Depends(get_db)) -> EnrollmentRead:
    learner = db.get(Learner, payload.learner_id)
    class_run = db.get(ClassRun, payload.class_run_id)
    if not learner or not class_run:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Learner or class run not found.")
    existing = (
        db.query(Enrollment)
        .filter(Enrollment.learner_id == payload.learner_id, Enrollment.class_run_id == payload.class_run_id)
        .first()
    )
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Learner already enrolled in this class run.")
    enrollment = Enrollment(learner_id=payload.learner_id, class_run_id=payload.class_run_id)
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    queue_enrollment_sync(enrollment)
    return EnrollmentRead.model_validate(enrollment)


@router.get("", response_model=list[EnrollmentRead], dependencies=[Depends(require_role(Role.OPS, Role.TRAINER, Role.ADMIN))])
def list_enrollments(db: Session = Depends(get_db)) -> list[EnrollmentRead]:
    enrollments = db.query(Enrollment).all()
    return [EnrollmentRead.model_validate(item) for item in enrollments]


@router.patch("/{enrollment_id}", response_model=EnrollmentRead, dependencies=[Depends(require_role(Role.OPS, Role.ADMIN))])
def update_enrollment(enrollment_id: str, payload: EnrollmentUpdate, db: Session = Depends(get_db)) -> EnrollmentRead:
    enrollment = db.get(Enrollment, enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enrollment not found.")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(enrollment, field, value)
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    queue_enrollment_sync(enrollment)
    return EnrollmentRead.model_validate(enrollment)
