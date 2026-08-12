from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

# docs/spec.md section 2 — the one task every demo and benchmark run targets.
CANONICAL_TASK = {
    "location": "ranchi",
    "category": "pizza",
    "veg_only": True,
    "size": "large",
    "max_price": 400,
    "min_restaurant_rating": 4.0,
    "max_delivery_time_minutes": 40,
    "available_now": True,
    "sort_by": "popularity",
}


def test_search_items_by_restaurant():
    response = client.post("/search_items", json={"restaurant_id": "r1"})
    assert response.status_code == 200
    assert len(response.json()["items"]) == 6


def test_search_items_filters_by_query():
    response = client.post(
        "/search_items", json={"restaurant_id": "r1", "query": "paneer"}
    )
    items = response.json()["items"]
    assert len(items) == 1
    assert items[0]["name"] == "Paneer Tikka"


def test_search_items_unknown_restaurant_returns_empty():
    response = client.post("/search_items", json={"restaurant_id": "nowhere"})
    assert response.json()["items"] == []


def test_search_spans_restaurants_when_restaurant_id_omitted():
    response = client.post(
        "/search_items", json={"location": "ranchi", "category": "pizza"}
    )
    items = response.json()["items"]
    assert len({i["restaurant_id"] for i in items}) > 1


def test_items_carry_their_restaurant_context():
    response = client.post("/search_items", json={"restaurant_id": "r9", "size": "large"})
    item = response.json()["items"][0]
    assert item["restaurant_name"] == "Slice of Italy"
    assert item["restaurant_rating"] == 4.1
    assert item["eta_minutes"] == 38


def test_canonical_task_has_exactly_one_right_answer():
    response = client.post("/search_items", json={**CANONICAL_TASK, "limit": 1})
    items = response.json()["items"]
    assert len(items) == 1
    assert items[0]["id"] == "i32"
    assert items[0]["name"] == "Veggie Supreme Pizza"
    assert items[0]["restaurant_name"] == "Slice of Italy"


def test_canonical_task_rejects_every_shortcut():
    response = client.post("/search_items", json=CANONICAL_TASK)
    ids = {i["id"] for i in response.json()["items"]}
    assert "i23" not in ids  # cheapest + most ordered, but 45 min ETA
    assert "i40" not in ids  # more orders than the answer, but out of stock
    assert "i31" not in ids  # high orders, but restaurant closed and 50 min ETA
    assert "i28" not in ids  # cheap and popular, but restaurant rated 3.8
    assert "i8" not in ids  # ₹420, over budget


def test_available_now_excludes_out_of_stock():
    in_stock_ids = {
        i["id"]
        for i in client.post(
            "/search_items", json={"restaurant_id": "r2", "available_now": True}
        ).json()["items"]
    }
    all_ids = {
        i["id"]
        for i in client.post("/search_items", json={"restaurant_id": "r2"}).json()["items"]
    }
    assert "i40" in all_ids
    assert "i40" not in in_stock_ids


def test_dietary_tags_filter_requires_all_tags():
    response = client.post(
        "/search_items",
        json={"location": "kolkata", "dietary_tags": ["egg_free", "gluten_free"]},
    )
    assert {i["id"] for i in response.json()["items"]} == {"i38", "i48"}


def test_sort_by_price_ascending():
    response = client.post(
        "/search_items", json={"location": "ranchi", "category": "pizza", "sort_by": "price_asc"}
    )
    prices = [i["price"] for i in response.json()["items"]]
    assert prices == sorted(prices)
