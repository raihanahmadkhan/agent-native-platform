from fastapi import APIRouter

from app.capabilities.search_restaurants import search_restaurants
from app.schemas.restaurant import SearchRestaurantsInput, SearchRestaurantsOutput

router = APIRouter()


@router.post("/search_restaurants", response_model=SearchRestaurantsOutput)
def route_search_restaurants(input: SearchRestaurantsInput):
    return search_restaurants(input)
