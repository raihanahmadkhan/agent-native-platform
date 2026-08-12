from fastapi import APIRouter

from app.manifest_data import MANIFEST

router = APIRouter()


@router.get("/manifest")
def get_manifest():
    return MANIFEST
