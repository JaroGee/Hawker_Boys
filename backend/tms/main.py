from __future__ import annotations

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from tms.api.routes import api_router
from tms.infra.bootstrap import ensure_default_admin
from tms.infra.config import settings


def create_app() -> FastAPI:
    app = FastAPI(title="Hawker Boys TMS", version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    def startup_event() -> None:  # pragma: no cover - side effect
        ensure_default_admin()

    app.include_router(api_router)

    @app.get("/healthz", tags=["health"], include_in_schema=False)
    def healthz() -> dict[str, str]:
        return {"status": "ok", "env": settings.app_env}

    @app.get("/readiness", tags=["health"], include_in_schema=False)
    def readiness() -> dict[str, str]:
        return {"status": "ready"}

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run("tms.main:app", host=settings.api_host, port=settings.api_port, reload=True)
