from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_search_by_location():
    response = client.post("/search_restaurants", json={"location": "ranchi"})
    assert response.status_code == 200
    data = response.json()
    assert len(data["restaurants"]) == 8


def test_search_filters_by_cuisine():
    response = client.post(
        "/search_restaurants", json={"location": "ranchi", "cuisine": "italian"}
    )
    names = [r["name"] for r in response.json()["restaurants"]]
    assert sorted(names) == ["Napoli Express", "Pizza Corner", "Slice of Italy"]


def test_search_unknown_location_returns_empty():
    response = client.post("/search_restaurants", json={"location": "nowhere"})
    assert response.json()["restaurants"] == []


def test_filters_by_min_rating():
    response = client.post(
        "/search_restaurants", json={"location": "ranchi", "min_rating": 4.5}
    )
    assert {r["id"] for r in response.json()["restaurants"]} == {"r1", "r5"}


def test_open_now_excludes_closed_restaurant():
    response = client.post(
        "/search_restaurants", json={"location": "ranchi", "open_now": True}
    )
    ids = {r["id"] for r in response.json()["restaurants"]}
    assert "r8" not in ids
    assert len(ids) == 7


def test_veg_only_filter():
    response = client.post(
        "/search_restaurants", json={"location": "ranchi", "veg_only": True}
    )
    restaurants = response.json()["restaurants"]
    assert len(restaurants) == 1
    assert restaurants[0]["name"] == "Green Leaf"


def test_sort_by_popularity():
    response = client.post(
        "/search_restaurants", json={"location": "ranchi", "sort_by": "popularity"}
    )
    assert response.json()["restaurants"][0]["id"] == "r2"
