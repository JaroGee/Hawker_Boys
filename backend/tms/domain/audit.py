from __future__ import annotations

import uuid

from sqlalchemy.orm import Session

from tms.domain import models


def record_audit(
    db: Session,
    *,
    action: models.AuditActionEnum,
    entity_type: str,
    entity_id: str,
    performed_by: uuid.UUID | None,
    context: str | None = None,
) -> None:
    entry = models.AuditTrail(
        performed_by=performed_by,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        context=context,
    )
    db.add(entry)
