from pydantic import BaseModel


class SearchItemsInput(BaseModel):
    restaurant_id: str | None = None  # omit to search across restaurants
    location: str | None = None
    query: str | None = None
    category: str | None = None  # pizza | curry | noodles | dessert | drink | starter
    veg_only: bool | None = None
    size: str | None = None  # regular | medium | large
    max_price: float | None = None
    max_spice_level: int | None = None
    dietary_tags: list[str] | None = None  # jain | egg_free | gluten_free
    available_now: bool | None = None
    min_restaurant_rating: float | None = None
    max_delivery_time_minutes: int | None = None
    sort_by: str | None = None  # popularity | price_asc | price_desc | rating
    limit: int | None = None


class Item(BaseModel):
    id: str
    name: str
    price: float
    veg: bool
    size: str
    category: str
    spice_level: int
    dietary_tags: list[str]
    total_orders: int
    in_stock: bool
    restaurant_id: str
    restaurant_name: str
    restaurant_rating: float
    eta_minutes: int


class SearchItemsOutput(BaseModel):
    items: list[Item]
