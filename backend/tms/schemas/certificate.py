from __future__ import annotations

import datetime as dt
import uuid

from pydantic import BaseModel


class CertificateCreate(BaseModel):
    enrollment_id: uuid.UUID
    certificate_url: str
    issued_on: dt.date | None = None


class CertificateRead(CertificateCreate):
    id: uuid.UUID
    issued_on: dt.date
    created_at: dt.datetime
    updated_at: dt.datetime

    class Config:
        from_attributes = True
