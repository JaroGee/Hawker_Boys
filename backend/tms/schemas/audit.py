from __future__ import annotations

import datetime as dt
import uuid

from pydantic import BaseModel


class AuditTrailRead(BaseModel):
    id: uuid.UUID
    performed_by: uuid.UUID | None
    action: str
    entity_type: str
    entity_id: str
    timestamp: dt.datetime
    context: str | None

    class Config:
        from_attributes = True
