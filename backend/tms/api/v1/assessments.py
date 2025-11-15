from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from tms.auth.security import require_trainer_or_admin
from tms.domain import models, record_audit
from tms.domain.models import AuditActionEnum
from tms.infra.database import get_db
from tms.schemas import AssessmentCreate, AssessmentRead, TokenPayload

router = APIRouter()


@router.get("/", response_model=list[AssessmentRead], dependencies=[Depends(require_trainer_or_admin)])
def list_assessments(db: Session = Depends(get_db)) -> list[AssessmentRead]:
    assessments = db.query(models.Assessment).all()
    return [AssessmentRead.model_validate(assessment) for assessment in assessments]


@router.post("/", response_model=AssessmentRead, status_code=status.HTTP_201_CREATED)
def create_assessment(
    payload: AssessmentCreate,
    db: Session = Depends(get_db),
    token: TokenPayload = Depends(require_trainer_or_admin),
) -> AssessmentRead:
    enrollment = db.get(models.Enrollment, payload.enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Enrollment not found")

    assessment = models.Assessment(
        enrollment=enrollment,
        score=payload.score,
        remarks=payload.remarks,
        assessed_on=payload.assessed_on or enrollment.enrollment_date,
    )
    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    record_audit(
        db,
        action=AuditActionEnum.CREATE,
        entity_type="assessment",
        entity_id=str(assessment.id),
        performed_by=uuid.UUID(token.sub),
    )
    db.commit()

    return AssessmentRead.model_validate(assessment)
