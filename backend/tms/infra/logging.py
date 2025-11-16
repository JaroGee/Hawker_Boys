from __future__ import annotations

import logging
import os
import sys
from typing import Any

import structlog

from tms.infra.config import settings


def configure_logging() -> None:
    log_context = os.getenv("HB_LOG_CONTEXT", "api").upper()

    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format=f"HB-{log_context} %(asctime)s %(levelname)s [%(name)s] %(message)s",
        stream=sys.stdout,
    )

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    return structlog.get_logger(name)
