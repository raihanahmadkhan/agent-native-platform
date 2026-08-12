from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_manifest_returns_200():
    response = client.get("/manifest")
    assert response.status_code == 200


def test_manifest_lists_search_restaurants():
    response = client.get("/manifest")
    names = [c["name"] for c in response.json()["capabilities"]]
    assert "search_restaurants" in names
