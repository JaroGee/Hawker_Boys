from __future__ import annotations

from fastapi import FastAPI

from tms.api.routers import register_routes
from tms.infra.config import settings
from tms.infra.logging import configure_logging

configure_logging()

app = FastAPI(title=settings.app_name)
register_routes(app)


@app.get("/healthz", tags=["health"])
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/readiness", tags=["health"])
def readiness() -> dict[str, str]:
    return {"status": "ready"}
