from __future__ import annotations

from fastapi import APIRouter, Header, HTTPException, Response, status

from tms.infra.config import settings

router = APIRouter()


@router.post("/test-webhook", status_code=status.HTTP_204_NO_CONTENT)
def test_webhook(secret: str | None = Header(None, alias="X-SSG-Webhook-Secret")) -> Response:
    expected = settings.ssg_webhook_secret
    if not expected:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Webhook secret not configured")
    if secret != expected:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid webhook secret")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
