from __future__ import annotations

from enum import Enum
from typing import Annotated

from fastapi import Depends, Header, HTTPException, status


class Role(str, Enum):
    ADMIN = "admin"
    TRAINER = "trainer"
    OPS = "ops"
    LEARNER = "learner"


def authorize(x_role: Annotated[str | None, Header(alias="X-Role")]) -> Role:
    if x_role is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing role header.")
    try:
        return Role(x_role)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role header.") from exc
