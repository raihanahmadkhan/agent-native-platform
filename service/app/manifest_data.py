MANIFEST = {
    "service": "FoodHub",
    "capabilities": [
        {
            "name": "search_restaurants",
            "category": "READ",
            "description": "Find restaurants by location, cuisine, delivery time, and rating.",
            "input_schema": {
                "location": "string, required",
                "cuisine": "string, optional",
                "max_delivery_time_minutes": "integer, optional",
                "min_rating": "number, optional",
            },
            "output_schema": {
                "restaurants": "list of {id, name, cuisine, rating, eta_minutes}",
            },
        },
    ],
}
