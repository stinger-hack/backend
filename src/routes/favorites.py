from fastapi import APIRouter
from fastapi.responses import UJSONResponse

showcase_router = APIRouter()


@showcase_router.post("/favorite")
async def showcase_categories() -> str:
    response = await categories_service()
    return UJSONResponse({'categories': response})


@showcase_router.get("/favorite")
async def showcase_categories() -> str:
    response = await categories_service()
    return UJSONResponse({'categories': response})


@showcase_router.delete("/favorite")
async def showcase_categories() -> str:
    response = await categories_service()
    return UJSONResponse({'categories': response})