from app.data.seed_restaurants import RESTAURANTS
from app.schemas.restaurant import Restaurant, SearchRestaurantsInput, SearchRestaurantsOutput


def search_restaurants(input: SearchRestaurantsInput) -> SearchRestaurantsOutput:
    """
    READ capability. No auth required. No policy check needed.
    See docs/spec.md section 3.1 for the schema contract.
    """
    results = [r for r in RESTAURANTS if r["location"].lower() == input.location.lower()]

    if input.cuisine:
        results = [r for r in results if r["cuisine"].lower() == input.cuisine.lower()]

    if input.max_delivery_time_minutes is not None:
        results = [r for r in results if r["eta_minutes"] <= input.max_delivery_time_minutes]

    if input.min_rating is not None:
        results = [r for r in results if r["rating"] >= input.min_rating]

    return SearchRestaurantsOutput(restaurants=[Restaurant(**r) for r in results])
