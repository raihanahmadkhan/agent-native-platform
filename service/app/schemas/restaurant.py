from pydantic import BaseModel


class SearchRestaurantsInput(BaseModel):
    location: str
    cuisine: str | None = None
    max_delivery_time_minutes: int | None = None
    min_rating: float | None = None


class Restaurant(BaseModel):
    id: str
    name: str
    cuisine: str
    rating: float
    eta_minutes: int


class SearchRestaurantsOutput(BaseModel):
    restaurants: list[Restaurant]
