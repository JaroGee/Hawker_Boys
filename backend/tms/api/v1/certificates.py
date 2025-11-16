from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from tms.api.utils import apply_text_search, paginate, resolve_sort
from tms.auth.security import require_ops_or_admin
from tms.domain import models, record_audit
from tms.domain.models import AuditActionEnum
from tms.infra.database import get_db
from tms.schemas import CertificateCreate, CertificateRead, PaginatedResponse, TokenPayload

router = APIRouter()


@router.get(
    "/",
    response_model=PaginatedResponse[CertificateRead],
    dependencies=[Depends(require_ops_or_admin)],
)
def list_certificates(
    q: str | None = Query(None, description="Filter by learner or class run"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    sort: str | None = Query("-issued_on"),
    db: Session = Depends(get_db),
) -> PaginatedResponse[CertificateRead]:
    query = (
        db.query(models.Certificate)
        .join(models.Certificate.enrollment)
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
            "issued_on": models.Certificate.issued_on,
            "created_at": models.Certificate.created_at,
        },
        "-issued_on",
    )
    if sort_columns:
        query = query.order_by(*sort_columns)
    items, total = paginate(query, page, page_size)
    return PaginatedResponse[CertificateRead](
        items=[CertificateRead.model_validate(certificate) for certificate in items],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.post("/", response_model=CertificateRead, status_code=status.HTTP_201_CREATED)
def create_certificate(
    payload: CertificateCreate,
    db: Session = Depends(get_db),
    token: TokenPayload = Depends(require_ops_or_admin),
) -> CertificateRead:
    enrollment = db.get(models.Enrollment, payload.enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Enrollment not found")

    certificate = models.Certificate(
        enrollment=enrollment,
        certificate_url=payload.certificate_url,
        issued_on=payload.issued_on or enrollment.enrollment_date,
    )
    db.add(certificate)
    db.commit()
    db.refresh(certificate)

    record_audit(
        db,
        action=AuditActionEnum.CREATE,
        entity_type="certificate",
        entity_id=str(certificate.id),
        performed_by=uuid.UUID(token.sub),
    )
    db.commit()

    return CertificateRead.model_validate(certificate)
