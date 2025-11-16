from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from tms.api.utils import apply_text_search, paginate, resolve_sort
from tms.auth.security import require_admin
from tms.domain import models
from tms.infra.database import get_db
from tms.schemas import AuditTrailRead, PaginatedResponse

router = APIRouter()


@router.get(
    "/",
    response_model=PaginatedResponse[AuditTrailRead],
    dependencies=[Depends(require_admin)],
)
def list_audit_trails(
    q: str | None = Query(None, description="Filter by entity type or performer"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    sort: str | None = Query("-timestamp"),
    db: Session = Depends(get_db),
) -> PaginatedResponse[AuditTrailRead]:
    query = db.query(models.AuditTrail)
    query = apply_text_search(
        query,
        [models.AuditTrail.entity_type, models.AuditTrail.entity_id],
        q,
    )
    sort_columns = resolve_sort(
        sort,
        {
            "timestamp": models.AuditTrail.timestamp,
            "action": models.AuditTrail.action,
        },
        "-timestamp",
    )
    if sort_columns:
        query = query.order_by(*sort_columns)
    items, total = paginate(query, page, page_size)
    return PaginatedResponse[AuditTrailRead](
        items=[AuditTrailRead.model_validate(trail) for trail in items],
        total=total,
        page=page,
        page_size=page_size,
    )
