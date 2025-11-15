from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from tms.auth.security import require_admin
from tms.domain import models
from tms.infra.database import get_db
from tms.schemas import AuditTrailRead

router = APIRouter()


@router.get("/", response_model=list[AuditTrailRead], dependencies=[Depends(require_admin)])
def list_audit_trails(db: Session = Depends(get_db)) -> list[AuditTrailRead]:
    trails = db.query(models.AuditTrail).order_by(models.AuditTrail.timestamp.desc()).limit(200).all()
    return [AuditTrailRead.model_validate(trail) for trail in trails]
