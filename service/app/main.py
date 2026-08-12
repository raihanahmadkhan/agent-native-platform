from fastapi import FastAPI

from app.config import settings
from app.routers import items, manifest, restaurants

app = FastAPI(title=settings.app_name)

app.include_router(manifest.router)
app.include_router(restaurants.router)
app.include_router(items.router)


@app.get("/")
def root():
    return {"status": "ok", "service": settings.app_name}
