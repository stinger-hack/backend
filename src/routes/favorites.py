from fastapi import APIRouter
from fastapi.responses import UJSONResponse
from starlette.requests import Request
from starlette.responses import JSONResponse

from services.add_favorite import add_favorite_service
from services.get_favorites import get_favorites_service
from services.delete_favorite import delete_favorite_service

favorite_router = APIRouter()


@favorite_router.post("/favorite")
async def showcase_categories(request: Request) -> str:
    req: dict = await request.json()
    startup_id = req.get('startup_id')
    await add_favorite_service(startup_id)
    return UJSONResponse({'msg': 'insert successful'})


@favorite_router.get("/favorite")
async def showcase_categories() -> str:
    response = await get_favorites_service()
    return UJSONResponse({'favorite': response})


@favorite_router.delete("/favorite")
async def showcase_categories(request: Request) -> str:
    req: dict = await request.json()
    startup_id = req.get('startup_id')
    await delete_favorite_service(startup_id)
    return JSONResponse({'categories': "response"})