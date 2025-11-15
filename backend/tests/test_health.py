from fastapi.testclient import TestClient

from tms.api import app


def test_health() -> None:
    client = TestClient(app)
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
