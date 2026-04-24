from fastapi.testclient import TestClient

from app.main import create_app


def test_health():
    client = TestClient(create_app())
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_fireflies_transcript_503_without_api_key():
    client = TestClient(create_app())
    r = client.post(
        "/tools/read/fireflies/transcript",
        json={"transcript_id": "test-transcript-id"},
        headers={"X-Internal-API-Key": "dev-change-me"},
    )
    assert r.status_code == 503
    assert "FIREFLIES_API_KEY" in r.json().get("detail", "")
