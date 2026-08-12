MANIFEST = {
    "service": "FoodHub",
    "capabilities": [
        {
            "name": "search_restaurants",
            "category": "READ",
            "description": "Find restaurants by location, cuisine, rating, delivery time, cost, distance, offers, and opening status.",
            "input_schema": {
                "location": "string, required",
                "cuisine": "string, optional",
                "max_delivery_time_minutes": "integer, optional",
                "min_rating": "number, optional",
                "veg_only": "boolean, optional",
                "max_cost_for_two": "integer, optional",
                "max_distance_km": "number, optional",
                "open_now": "boolean, optional",
                "has_offers": "boolean, optional",
                "sort_by": "string, optional — rating | delivery_time | cost | popularity",
            },
            "output_schema": {
                "restaurants": (
                    "list of {id, name, cuisine, rating, eta_minutes, cost_for_two, "
                    "distance_km, is_open, offer_text, total_orders, veg_only}"
                ),
            },
        },
        {
            "name": "search_items",
            "category": "READ",
            "description": (
                "Find menu items across one restaurant or every restaurant at once. "
                "Filter by name, category, diet, size, price, spice, availability, "
                "restaurant rating and delivery time; sort by popularity or price."
            ),
            "input_schema": {
                "restaurant_id": "string, optional — omit to search across restaurants",
                "location": "string, optional — scopes a cross-restaurant search",
                "query": "string, optional",
                "category": "string, optional — pizza | curry | noodles | dessert | drink | starter",
                "veg_only": "boolean, optional",
                "size": "string, optional — regular | medium | large",
                "max_price": "number, optional",
                "max_spice_level": "integer, optional — 0..3",
                "dietary_tags": "list of string, optional — jain | egg_free | gluten_free",
                "available_now": "boolean, optional",
                "min_restaurant_rating": "number, optional",
                "max_delivery_time_minutes": "integer, optional",
                "sort_by": "string, optional — popularity | price_asc | price_desc | rating",
                "limit": "integer, optional",
            },
            "output_schema": {
                "items": (
                    "list of {id, name, price, veg, size, category, spice_level, "
                    "dietary_tags, total_orders, in_stock, restaurant_id, "
                    "restaurant_name, restaurant_rating, eta_minutes}"
                ),
            },
        },
    ],
}
