from fastapi import APIRouter

from app.capabilities.search_items import search_items
from app.schemas.item import SearchItemsInput, SearchItemsOutput

router = APIRouter()


@router.post("/search_items", response_model=SearchItemsOutput)
def route_search_items(input: SearchItemsInput):
    return search_items(input)
