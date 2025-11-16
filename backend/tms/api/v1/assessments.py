from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from tms.api.utils import apply_text_search, paginate, resolve_sort
from tms.auth.security import require_trainer_or_admin
from tms.domain import models, record_audit
from tms.domain.models import AuditActionEnum
from tms.infra.database import get_db
from tms.schemas import AssessmentCreate, AssessmentRead, PaginatedResponse, TokenPayload

router = APIRouter()


@router.get(
    "/",
    response_model=PaginatedResponse[AssessmentRead],
    dependencies=[Depends(require_trainer_or_admin)],
)
def list_assessments(
    q: str | None = Query(None, description="Filter by learner or class run"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    sort: str | None = Query("-assessed_on"),
    db: Session = Depends(get_db),
) -> PaginatedResponse[AssessmentRead]:
    query = (
        db.query(models.Assessment)
        .join(models.Assessment.enrollment)
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
            "assessed_on": models.Assessment.assessed_on,
            "score": models.Assessment.score,
            "created_at": models.Assessment.created_at,
        },
        "-assessed_on",
    )
    if sort_columns:
        query = query.order_by(*sort_columns)
    items, total = paginate(query, page, page_size)
    return PaginatedResponse[AssessmentRead](
        items=[AssessmentRead.model_validate(assessment) for assessment in items],
        total=total,
        page=page,
        page_size=page_size,
    )


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
