from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_healthz():
    response = client.get("/healthz")
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "ok"


def test_shorten_and_redirect():
    target = "https://example.com/"
    response = client.post("/shorten", json={"url": target})
    assert response.status_code == 200
    data = response.json()
    assert "short_id" in data
    assert data["original_url"] == target

    short_id = data["short_id"]
    redirect_resp = client.get(f"/{short_id}", follow_redirects=False)
    assert redirect_resp.status_code == 307
    assert redirect_resp.headers["location"] == target


def test_not_found():
    response = client.get("/unknown_url_id")
    assert response.status_code == 404
