# Temporary in-memory data source. Replace with a real DB query once
# service/app/models/ + a DB connection are introduced (see docs/architecture.md
# "Build order" step 4 — that's when create_order needs real persistence).
#
# This data is deliberately shaped so the canonical task in docs/spec.md section 2
# ("large veg pizza under ₹400, 4+ rated, Ranchi, under 40 min, most ordered")
# has exactly ONE correct answer — i32, Veggie Supreme (Large) at Slice of Italy —
# and so that every obvious shortcut lands on a different, wrong item:
#
#   i23  cheapest AND globally most-ordered large veg pizza  → restaurant ETA is 45 min
#   i40  most-ordered pizza that passes every other filter   → out of stock
#   i31  very high orders, price/size/rating all fine        → restaurant closed, ETA 50
#   i18  cheapest qualifying, at the highest-rated place     → only 5100 orders
#   i28  high orders, cheap, in stock, fast                  → restaurant rated 3.8
#   i8   most-ordered pizza at the fastest restaurant        → ₹420, over budget
#
# Do not "clean up" these outliers — they are the benchmark's discriminating power.

ITEMS = [
    # --- r1 Spice Route (indian, ranchi, 4.5★, 30 min) ---
    {"id": "i1", "restaurant_id": "r1", "name": "Paneer Tikka", "price": 220.0,
     "veg": True, "size": "regular", "category": "starter", "spice_level": 2,
     "dietary_tags": [], "total_orders": 4200, "in_stock": True},
    {"id": "i2", "restaurant_id": "r1", "name": "Butter Chicken", "price": 280.0,
     "veg": False, "size": "regular", "category": "curry", "spice_level": 1,
     "dietary_tags": [], "total_orders": 6800, "in_stock": True},
    {"id": "i3", "restaurant_id": "r1", "name": "Dal Makhani", "price": 180.0,
     "veg": True, "size": "regular", "category": "curry", "spice_level": 1,
     "dietary_tags": ["jain"], "total_orders": 5100, "in_stock": True},
    {"id": "i4", "restaurant_id": "r1", "name": "Gulab Jamun", "price": 90.0,
     "veg": True, "size": "regular", "category": "dessert", "spice_level": 0,
     "dietary_tags": ["egg_free"], "total_orders": 3300, "in_stock": True},
    {"id": "i5", "restaurant_id": "r1", "name": "Masala Chai", "price": 40.0,
     "veg": True, "size": "regular", "category": "drink", "spice_level": 0,
     "dietary_tags": ["gluten_free", "egg_free"], "total_orders": 2100, "in_stock": True},
    {"id": "i44", "restaurant_id": "r1", "name": "Rogan Josh", "price": 300.0,
     "veg": False, "size": "regular", "category": "curry", "spice_level": 2,
     "dietary_tags": [], "total_orders": 3700, "in_stock": True},

    # --- r2 Pizza Corner (italian, ranchi, 4.2★, 25 min) ---
    {"id": "i6", "restaurant_id": "r2", "name": "Margherita Pizza", "price": 220.0,
     "veg": True, "size": "medium", "category": "pizza", "spice_level": 0,
     "dietary_tags": ["egg_free"], "total_orders": 5600, "in_stock": True},
    {"id": "i7", "restaurant_id": "r2", "name": "Margherita Pizza", "price": 380.0,
     "veg": True, "size": "large", "category": "pizza", "spice_level": 0,
     "dietary_tags": ["egg_free"], "total_orders": 3400, "in_stock": True},
    {"id": "i8", "restaurant_id": "r2", "name": "Farmhouse Pizza", "price": 420.0,
     "veg": True, "size": "large", "category": "pizza", "spice_level": 1,
     "dietary_tags": [], "total_orders": 4100, "in_stock": True},
    {"id": "i9", "restaurant_id": "r2", "name": "Pepperoni Pizza", "price": 300.0,
     "veg": False, "size": "medium", "category": "pizza", "spice_level": 2,
     "dietary_tags": [], "total_orders": 4800, "in_stock": True},
    {"id": "i10", "restaurant_id": "r2", "name": "Garlic Bread", "price": 120.0,
     "veg": True, "size": "regular", "category": "starter", "spice_level": 0,
     "dietary_tags": [], "total_orders": 3900, "in_stock": True},
    {"id": "i40", "restaurant_id": "r2", "name": "Veg Loaded Pizza", "price": 370.0,
     "veg": True, "size": "large", "category": "pizza", "spice_level": 1,
     "dietary_tags": [], "total_orders": 8900, "in_stock": False},
    {"id": "i41", "restaurant_id": "r2", "name": "Cold Coffee", "price": 110.0,
     "veg": True, "size": "regular", "category": "drink", "spice_level": 0,
     "dietary_tags": [], "total_orders": 2400, "in_stock": True},

    # --- r3 Dragon Wok (chinese, ranchi, 4.0★, 40 min) ---
    {"id": "i11", "restaurant_id": "r3", "name": "Kung Pao Chicken", "price": 260.0,
     "veg": False, "size": "regular", "category": "curry", "spice_level": 3,
     "dietary_tags": [], "total_orders": 3100, "in_stock": True},
    {"id": "i12", "restaurant_id": "r3", "name": "Veg Hakka Noodles", "price": 190.0,
     "veg": True, "size": "regular", "category": "noodles", "spice_level": 1,
     "dietary_tags": ["egg_free"], "total_orders": 4400, "in_stock": True},
    {"id": "i13", "restaurant_id": "r3", "name": "Chilli Paneer", "price": 230.0,
     "veg": True, "size": "regular", "category": "starter", "spice_level": 3,
     "dietary_tags": [], "total_orders": 3800, "in_stock": True},
    {"id": "i14", "restaurant_id": "r3", "name": "Schezwan Fried Rice", "price": 210.0,
     "veg": True, "size": "large", "category": "noodles", "spice_level": 3,
     "dietary_tags": [], "total_orders": 2700, "in_stock": True},
    {"id": "i46", "restaurant_id": "r3", "name": "Dim Sum Platter", "price": 240.0,
     "veg": True, "size": "regular", "category": "starter", "spice_level": 1,
     "dietary_tags": [], "total_orders": 2300, "in_stock": True},

    # --- r4 Bengal Bites (indian, kolkata, 4.7★, 20 min) ---
    {"id": "i15", "restaurant_id": "r4", "name": "Kosha Mangsho", "price": 320.0,
     "veg": False, "size": "regular", "category": "curry", "spice_level": 2,
     "dietary_tags": [], "total_orders": 5900, "in_stock": True},
    {"id": "i16", "restaurant_id": "r4", "name": "Aloo Posto", "price": 170.0,
     "veg": True, "size": "regular", "category": "curry", "spice_level": 1,
     "dietary_tags": ["jain", "gluten_free"], "total_orders": 4600, "in_stock": True},
    {"id": "i17", "restaurant_id": "r4", "name": "Mishti Doi", "price": 80.0,
     "veg": True, "size": "regular", "category": "dessert", "spice_level": 0,
     "dietary_tags": ["gluten_free"], "total_orders": 6200, "in_stock": True},
    {"id": "i47", "restaurant_id": "r4", "name": "Fish Curry", "price": 290.0,
     "veg": False, "size": "regular", "category": "curry", "spice_level": 2,
     "dietary_tags": ["gluten_free"], "total_orders": 4100, "in_stock": True},

    # --- r5 Napoli Express (italian, ranchi, 4.6★, 35 min) ---
    {"id": "i18", "restaurant_id": "r5", "name": "Margherita Pizza", "price": 350.0,
     "veg": True, "size": "large", "category": "pizza", "spice_level": 0,
     "dietary_tags": ["egg_free"], "total_orders": 5100, "in_stock": True},
    {"id": "i19", "restaurant_id": "r5", "name": "Margherita Pizza", "price": 210.0,
     "veg": True, "size": "medium", "category": "pizza", "spice_level": 0,
     "dietary_tags": ["egg_free"], "total_orders": 6700, "in_stock": True},
    {"id": "i20", "restaurant_id": "r5", "name": "Veg Exotica Pizza", "price": 395.0,
     "veg": True, "size": "large", "category": "pizza", "spice_level": 1,
     "dietary_tags": [], "total_orders": 2900, "in_stock": True},
    {"id": "i21", "restaurant_id": "r5", "name": "Chicken Supreme Pizza", "price": 450.0,
     "veg": False, "size": "large", "category": "pizza", "spice_level": 2,
     "dietary_tags": [], "total_orders": 3500, "in_stock": True},
    {"id": "i22", "restaurant_id": "r5", "name": "Tiramisu", "price": 180.0,
     "veg": True, "size": "regular", "category": "dessert", "spice_level": 0,
     "dietary_tags": [], "total_orders": 1900, "in_stock": True},
    {"id": "i43", "restaurant_id": "r5", "name": "Garlic Breadsticks", "price": 130.0,
     "veg": True, "size": "regular", "category": "starter", "spice_level": 0,
     "dietary_tags": [], "total_orders": 3600, "in_stock": True},

    # --- r6 Green Leaf (indian, ranchi, 4.4★, 45 min — veg only) ---
    {"id": "i23", "restaurant_id": "r6", "name": "Corn & Cheese Pizza", "price": 300.0,
     "veg": True, "size": "large", "category": "pizza", "spice_level": 0,
     "dietary_tags": ["egg_free"], "total_orders": 9500, "in_stock": True},
    {"id": "i24", "restaurant_id": "r6", "name": "Veg Manchurian", "price": 200.0,
     "veg": True, "size": "regular", "category": "starter", "spice_level": 2,
     "dietary_tags": [], "total_orders": 4300, "in_stock": True},
    {"id": "i25", "restaurant_id": "r6", "name": "Paneer Butter Masala", "price": 250.0,
     "veg": True, "size": "regular", "category": "curry", "spice_level": 1,
     "dietary_tags": ["jain"], "total_orders": 5400, "in_stock": True},
    {"id": "i45", "restaurant_id": "r6", "name": "Veg Fried Rice", "price": 180.0,
     "veg": True, "size": "regular", "category": "noodles", "spice_level": 1,
     "dietary_tags": [], "total_orders": 3900, "in_stock": True},

    # --- r7 Wok & Roll (chinese, ranchi, 3.8★, 28 min) ---
    {"id": "i26", "restaurant_id": "r7", "name": "Chicken Noodles", "price": 220.0,
     "veg": False, "size": "regular", "category": "noodles", "spice_level": 2,
     "dietary_tags": [], "total_orders": 2600, "in_stock": True},
    {"id": "i27", "restaurant_id": "r7", "name": "Veg Spring Roll", "price": 150.0,
     "veg": True, "size": "regular", "category": "starter", "spice_level": 1,
     "dietary_tags": ["egg_free"], "total_orders": 3100, "in_stock": True},
    {"id": "i28", "restaurant_id": "r7", "name": "Veg Pizza", "price": 280.0,
     "veg": True, "size": "large", "category": "pizza", "spice_level": 0,
     "dietary_tags": [], "total_orders": 7000, "in_stock": True},
    {"id": "i49", "restaurant_id": "r7", "name": "Veg Momos", "price": 140.0,
     "veg": True, "size": "regular", "category": "starter", "spice_level": 1,
     "dietary_tags": [], "total_orders": 3400, "in_stock": True},

    # --- r8 Tandoor Tales (indian, ranchi, 4.3★, 50 min — CLOSED) ---
    {"id": "i29", "restaurant_id": "r8", "name": "Tandoori Chicken", "price": 340.0,
     "veg": False, "size": "large", "category": "starter", "spice_level": 2,
     "dietary_tags": [], "total_orders": 4900, "in_stock": True},
    {"id": "i30", "restaurant_id": "r8", "name": "Veg Seekh Kebab", "price": 240.0,
     "veg": True, "size": "regular", "category": "starter", "spice_level": 2,
     "dietary_tags": [], "total_orders": 2800, "in_stock": True},
    {"id": "i31", "restaurant_id": "r8", "name": "Margherita Pizza", "price": 360.0,
     "veg": True, "size": "large", "category": "pizza", "spice_level": 0,
     "dietary_tags": [], "total_orders": 8800, "in_stock": True},
    {"id": "i50", "restaurant_id": "r8", "name": "Naan Basket", "price": 120.0,
     "veg": True, "size": "regular", "category": "starter", "spice_level": 0,
     "dietary_tags": [], "total_orders": 2900, "in_stock": True},

    # --- r9 Slice of Italy (italian, ranchi, 4.1★, 38 min) ---
    {"id": "i32", "restaurant_id": "r9", "name": "Veggie Supreme Pizza", "price": 390.0,
     "veg": True, "size": "large", "category": "pizza", "spice_level": 1,
     "dietary_tags": [], "total_orders": 8200, "in_stock": True},
    {"id": "i33", "restaurant_id": "r9", "name": "Veggie Supreme Pizza", "price": 240.0,
     "veg": True, "size": "medium", "category": "pizza", "spice_level": 1,
     "dietary_tags": [], "total_orders": 5300, "in_stock": True},
    {"id": "i34", "restaurant_id": "r9", "name": "Paneer Tikka Pizza", "price": 410.0,
     "veg": True, "size": "large", "category": "pizza", "spice_level": 2,
     "dietary_tags": [], "total_orders": 6100, "in_stock": True},
    {"id": "i35", "restaurant_id": "r9", "name": "Pasta Alfredo", "price": 260.0,
     "veg": True, "size": "regular", "category": "noodles", "spice_level": 0,
     "dietary_tags": [], "total_orders": 3200, "in_stock": True},
    {"id": "i36", "restaurant_id": "r9", "name": "Choco Lava Cake", "price": 140.0,
     "veg": True, "size": "regular", "category": "dessert", "spice_level": 0,
     "dietary_tags": [], "total_orders": 4700, "in_stock": True},
    {"id": "i42", "restaurant_id": "r9", "name": "Lemonade", "price": 70.0,
     "veg": True, "size": "regular", "category": "drink", "spice_level": 0,
     "dietary_tags": ["gluten_free", "egg_free"], "total_orders": 1600, "in_stock": True},

    # --- r10 Sushi Den (japanese, kolkata, 4.8★, 32 min) ---
    {"id": "i37", "restaurant_id": "r10", "name": "Salmon Nigiri", "price": 480.0,
     "veg": False, "size": "regular", "category": "starter", "spice_level": 0,
     "dietary_tags": ["gluten_free"], "total_orders": 2200, "in_stock": True},
    {"id": "i38", "restaurant_id": "r10", "name": "Veg Maki Roll", "price": 320.0,
     "veg": True, "size": "regular", "category": "starter", "spice_level": 0,
     "dietary_tags": ["egg_free", "gluten_free"], "total_orders": 1800, "in_stock": True},
    {"id": "i39", "restaurant_id": "r10", "name": "Miso Soup", "price": 160.0,
     "veg": True, "size": "regular", "category": "starter", "spice_level": 0,
     "dietary_tags": ["gluten_free"], "total_orders": 1400, "in_stock": True},
    {"id": "i48", "restaurant_id": "r10", "name": "Green Tea", "price": 90.0,
     "veg": True, "size": "regular", "category": "drink", "spice_level": 0,
     "dietary_tags": ["gluten_free", "egg_free"], "total_orders": 900, "in_stock": True},
]
