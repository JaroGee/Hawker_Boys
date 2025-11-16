from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from tms.api.utils import apply_text_search, paginate, resolve_sort
from tms.auth.security import require_ops_or_admin
from tms.domain import models, record_audit
from tms.domain.models import AuditActionEnum
from tms.infra.database import get_db
from tms.schemas import LearnerCreate, LearnerRead, PaginatedResponse, TokenPayload

router = APIRouter()


@router.get(
    "/",
    response_model=PaginatedResponse[LearnerRead],
    dependencies=[Depends(require_ops_or_admin)],
)
def list_learners(
    q: str | None = Query(None, description="Filter by name or NRIC"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    sort: str | None = Query("-created_at"),
    db: Session = Depends(get_db),
) -> PaginatedResponse[LearnerRead]:
    query = db.query(models.Learner)
    query = apply_text_search(
        query,
        [models.Learner.given_name, models.Learner.family_name, models.Learner.masked_nric],
        q,
    )
    sort_columns = resolve_sort(
        sort,
        {
            "given_name": models.Learner.given_name,
            "family_name": models.Learner.family_name,
            "created_at": models.Learner.created_at,
        },
        "-created_at",
    )
    if sort_columns:
        query = query.order_by(*sort_columns)
    items, total = paginate(query, page, page_size)
    return PaginatedResponse[LearnerRead](
        items=[LearnerRead.model_validate(learner) for learner in items],
        total=total,
        page=page,
        page_size=page_size,
    )


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
