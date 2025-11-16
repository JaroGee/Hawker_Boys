from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from tms.api.utils import apply_text_search, paginate, resolve_sort
from tms.auth.security import require_ops_or_admin
from tms.domain import models
from tms.infra.database import get_db
from tms.schemas import ClassRunRead, PaginatedResponse

router = APIRouter()


@router.get(
    "/",
    response_model=PaginatedResponse[ClassRunRead],
    dependencies=[Depends(require_ops_or_admin)],
)
def list_class_runs(
    q: str | None = Query(None, description="Filter class runs by reference, course code, or course title."),
    course_id: uuid.UUID | None = Query(None, description="Filter by parent course."),
    status_filter: str | None = Query(None, alias="status", description="Filter by class run status."),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    sort: str | None = Query("-start_date"),
    db: Session = Depends(get_db),
) -> PaginatedResponse[ClassRunRead]:
    query = db.query(models.ClassRun).join(models.Course)
    query = apply_text_search(
        query,
        [models.ClassRun.reference_code, models.Course.title, models.Course.code],
        q,
    )
    if course_id:
        query = query.filter(models.ClassRun.course_id == course_id)
    if status_filter:
        try:
            status_value = models.ClassRunStatusEnum(status_filter)
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid status value") from exc
        query = query.filter(models.ClassRun.status == status_value)

    sort_columns = resolve_sort(
        sort,
        {
            "reference_code": models.ClassRun.reference_code,
            "start_date": models.ClassRun.start_date,
            "end_date": models.ClassRun.end_date,
            "created_at": models.ClassRun.created_at,
        },
        "-start_date",
    )
    if sort_columns:
        query = query.order_by(*sort_columns)

    items, total = paginate(query, page, page_size)
    runs = [ClassRunRead.model_validate(class_run) for class_run in items]
    return PaginatedResponse[ClassRunRead](items=runs, total=total, page=page, page_size=page_size)
