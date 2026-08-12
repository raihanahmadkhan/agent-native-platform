from pydantic import BaseModel


class SearchRestaurantsInput(BaseModel):
    location: str
    cuisine: str | None = None
    max_delivery_time_minutes: int | None = None
    min_rating: float | None = None
    veg_only: bool | None = None
    max_cost_for_two: int | None = None
    max_distance_km: float | None = None
    open_now: bool | None = None
    has_offers: bool | None = None
    sort_by: str | None = None  # rating | delivery_time | cost | popularity


class Restaurant(BaseModel):
    id: str
    name: str
    cuisine: str
    rating: float
    eta_minutes: int
    cost_for_two: int
    distance_km: float
    is_open: bool
    offer_text: str | None
    total_orders: int
    veg_only: bool


class SearchRestaurantsOutput(BaseModel):
    restaurants: list[Restaurant]
