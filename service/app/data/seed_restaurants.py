# Temporary in-memory data source. Replace with a real DB query once
# service/app/models/ + a DB connection are introduced (see docs/architecture.md
# "Build order" step 4 — that's when create_order needs real persistence).

RESTAURANTS = [
    {"id": "r1", "name": "Spice Route", "cuisine": "indian", "location": "ranchi",
     "rating": 4.5, "eta_minutes": 30},
    {"id": "r2", "name": "Pizza Corner", "cuisine": "italian", "location": "ranchi",
     "rating": 4.2, "eta_minutes": 25},
    {"id": "r3", "name": "Dragon Wok", "cuisine": "chinese", "location": "ranchi",
     "rating": 4.0, "eta_minutes": 40},
    {"id": "r4", "name": "Bengal Bites", "cuisine": "indian", "location": "kolkata",
     "rating": 4.7, "eta_minutes": 20},
]
