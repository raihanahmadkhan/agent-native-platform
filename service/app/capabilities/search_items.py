from app.data.seed_items import ITEMS
from app.data.seed_restaurants import RESTAURANTS
from app.schemas.item import Item, SearchItemsInput, SearchItemsOutput

RESTAURANTS_BY_ID = {r["id"]: r for r in RESTAURANTS}

SORT_KEYS = {
    "popularity": lambda i: -i["total_orders"],
    "price_asc": lambda i: i["price"],
    "price_desc": lambda i: -i["price"],
    "rating": lambda i: -RESTAURANTS_BY_ID[i["restaurant_id"]]["rating"],
}


def search_items(input: SearchItemsInput) -> SearchItemsOutput:
    """
    READ capability. No auth required. No policy check needed.
    See docs/spec.md section 4.2 for the schema contract.

    `restaurant_id` is optional — when omitted the search runs across every
    restaurant, which is the structural advantage over the browser path where
    each restaurant must be opened separately.

    `available_now` means the item is in stock AND its restaurant is currently
    open — i.e. "can I actually get this right now".
    """
    results = list(ITEMS)

    if input.restaurant_id:
        results = [i for i in results if i["restaurant_id"] == input.restaurant_id]

    if input.location:
        results = [
            i for i in results
            if RESTAURANTS_BY_ID[i["restaurant_id"]]["location"].lower()
            == input.location.lower()
        ]

    if input.query:
        results = [i for i in results if input.query.lower() in i["name"].lower()]

    if input.category:
        results = [i for i in results if i["category"] == input.category.lower()]

    if input.veg_only:
        results = [i for i in results if i["veg"]]

    if input.size:
        results = [i for i in results if i["size"] == input.size.lower()]

    if input.max_price is not None:
        results = [i for i in results if i["price"] <= input.max_price]

    if input.max_spice_level is not None:
        results = [i for i in results if i["spice_level"] <= input.max_spice_level]

    if input.dietary_tags:
        wanted = {t.lower() for t in input.dietary_tags}
        results = [i for i in results if wanted.issubset(set(i["dietary_tags"]))]

    if input.available_now:
        results = [
            i for i in results
            if i["in_stock"] and RESTAURANTS_BY_ID[i["restaurant_id"]]["is_open"]
        ]

    if input.min_restaurant_rating is not None:
        results = [
            i for i in results
            if RESTAURANTS_BY_ID[i["restaurant_id"]]["rating"] >= input.min_restaurant_rating
        ]

    if input.max_delivery_time_minutes is not None:
        results = [
            i for i in results
            if RESTAURANTS_BY_ID[i["restaurant_id"]]["eta_minutes"]
            <= input.max_delivery_time_minutes
        ]

    if input.sort_by in SORT_KEYS:
        results = sorted(results, key=SORT_KEYS[input.sort_by])

    if input.limit is not None:
        results = results[: input.limit]

    return SearchItemsOutput(items=[_to_item(i) for i in results])


def _to_item(row: dict) -> Item:
    restaurant = RESTAURANTS_BY_ID[row["restaurant_id"]]
    return Item(
        **row,
        restaurant_name=restaurant["name"],
        restaurant_rating=restaurant["rating"],
        eta_minutes=restaurant["eta_minutes"],
    )
