from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_search_by_location():
    response = client.post("/search_restaurants", json={"location": "ranchi"})
    assert response.status_code == 200
    data = response.json()
    assert len(data["restaurants"]) == 3


def test_search_filters_by_cuisine():
    response = client.post(
        "/search_restaurants", json={"location": "ranchi", "cuisine": "italian"}
    )
    data = response.json()
    assert len(data["restaurants"]) == 1
    assert data["restaurants"][0]["name"] == "Pizza Corner"


def test_search_unknown_location_returns_empty():
    response = client.post("/search_restaurants", json={"location": "nowhere"})
    assert response.json()["restaurants"] == []
