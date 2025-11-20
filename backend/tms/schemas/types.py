from __future__ import annotations

from typing import Annotated

from email_validator import EmailNotValidError, validate_email
from pydantic.functional_validators import AfterValidator


def _validate_local_email(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError("String required")
    try:
        return validate_email(value).normalized
    except EmailNotValidError as exc:  # pragma: no cover - email_validator already tested upstream
        lowered = value.strip().lower()
        if lowered.endswith(".local"):
            local_part, _, domain = lowered.partition("@")
            if not local_part or not domain:
                raise ValueError(str(exc)) from exc
            return f"{local_part}@{domain}"
        raise ValueError(str(exc)) from exc


LocalEmailStr = Annotated[str, AfterValidator(_validate_local_email)]
