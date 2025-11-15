from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from tms.auth.security import require_ops_or_admin
from tms.domain import models, record_audit
from tms.domain.models import AuditActionEnum
from tms.infra.database import get_db
from tms.schemas import LearnerCreate, LearnerRead, TokenPayload

router = APIRouter()


@router.get("/", response_model=list[LearnerRead], dependencies=[Depends(require_ops_or_admin)])
def list_learners(db: Session = Depends(get_db)) -> list[LearnerRead]:
    learners = db.query(models.Learner).all()
    return [LearnerRead.model_validate(learner) for learner in learners]


@router.post("/", response_model=LearnerRead, status_code=status.HTTP_201_CREATED)
def create_learner(
    payload: LearnerCreate,
    db: Session = Depends(get_db),
    token: TokenPayload = Depends(require_ops_or_admin),
) -> LearnerRead:
    learner = models.Learner(
        given_name=payload.given_name,
        family_name=payload.family_name,
        date_of_birth=payload.date_of_birth,
        contact_number=payload.contact_number,
        masked_nric=payload.masked_nric,
    )
    db.add(learner)
    db.commit()
    db.refresh(learner)

    record_audit(
        db,
        action=AuditActionEnum.CREATE,
        entity_type="learner",
        entity_id=str(learner.id),
        performed_by=uuid.UUID(token.sub),
    )
    db.commit()

    return LearnerRead.model_validate(learner)


@router.get("/{learner_id}", response_model=LearnerRead)
def read_learner(
    learner_id: uuid.UUID,
    db: Session = Depends(get_db),
    token: TokenPayload = Depends(require_ops_or_admin),
) -> LearnerRead:
    learner = db.get(models.Learner, learner_id)
    if not learner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Learner not found")

    record_audit(
        db,
        action=AuditActionEnum.ACCESS,
        entity_type="learner",
        entity_id=str(learner.id),
        performed_by=uuid.UUID(token.sub),
    )
    db.commit()

    return LearnerRead.model_validate(learner)
