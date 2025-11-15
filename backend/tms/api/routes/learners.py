from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from tms.api.dependencies import get_db, require_role
from tms.auth.authz import Role
from tms.domain.models import Learner
from tms.schemas import LearnerCreate, LearnerRead, LearnerUpdate

router = APIRouter(prefix="/learners")


@router.post("", response_model=LearnerRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_role(Role.OPS, Role.ADMIN))])
def create_learner(payload: LearnerCreate, db: Session = Depends(get_db)) -> LearnerRead:
    learner = Learner(**payload.model_dump())
    db.add(learner)
    db.commit()
    db.refresh(learner)
    return LearnerRead.model_validate(learner)


@router.get("", response_model=list[LearnerRead], dependencies=[Depends(require_role(Role.OPS, Role.TRAINER, Role.ADMIN))])
def list_learners(db: Session = Depends(get_db)) -> list[LearnerRead]:
    learners = db.query(Learner).all()
    return [LearnerRead.model_validate(learner) for learner in learners]


@router.get("/{learner_id}", response_model=LearnerRead, dependencies=[Depends(require_role(Role.OPS, Role.TRAINER, Role.ADMIN, Role.LEARNER))])
def get_learner(learner_id: str, db: Session = Depends(get_db)) -> LearnerRead:
    learner = db.get(Learner, learner_id)
    if not learner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Learner not found.")
    return LearnerRead.model_validate(learner)


@router.patch("/{learner_id}", response_model=LearnerRead, dependencies=[Depends(require_role(Role.OPS, Role.ADMIN))])
def update_learner(learner_id: str, payload: LearnerUpdate, db: Session = Depends(get_db)) -> LearnerRead:
    learner = db.get(Learner, learner_id)
    if not learner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Learner not found.")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(learner, field, value)
    db.add(learner)
    db.commit()
    db.refresh(learner)
    return LearnerRead.model_validate(learner)
