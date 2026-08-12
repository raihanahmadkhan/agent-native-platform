from app.data.seed_restaurants import RESTAURANTS
from app.schemas.restaurant import Restaurant, SearchRestaurantsInput, SearchRestaurantsOutput

SORT_KEYS = {
    "rating": lambda r: -r["rating"],
    "delivery_time": lambda r: r["eta_minutes"],
    "cost": lambda r: r["cost_for_two"],
    "popularity": lambda r: -r["total_orders"],
}


def search_restaurants(input: SearchRestaurantsInput) -> SearchRestaurantsOutput:
    """
    READ capability. No auth required. No policy check needed.
    See docs/spec.md section 4.1 for the schema contract.
    """
    results = [r for r in RESTAURANTS if r["location"].lower() == input.location.lower()]

    if input.cuisine:
        results = [r for r in results if r["cuisine"].lower() == input.cuisine.lower()]

    if input.max_delivery_time_minutes is not None:
        results = [r for r in results if r["eta_minutes"] <= input.max_delivery_time_minutes]

    if input.min_rating is not None:
        results = [r for r in results if r["rating"] >= input.min_rating]

    if input.veg_only:
        results = [r for r in results if r["veg_only"]]

    if input.max_cost_for_two is not None:
        results = [r for r in results if r["cost_for_two"] <= input.max_cost_for_two]

    if input.max_distance_km is not None:
        results = [r for r in results if r["distance_km"] <= input.max_distance_km]

    if input.open_now:
        results = [r for r in results if r["is_open"]]

    if input.has_offers:
        results = [r for r in results if r["offer_text"]]

    if input.sort_by in SORT_KEYS:
        results = sorted(results, key=SORT_KEYS[input.sort_by])

    return SearchRestaurantsOutput(restaurants=[Restaurant(**r) for r in results])
