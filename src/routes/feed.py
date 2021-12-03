from fastapi import APIRouter
from fastapi.params import Depends
from settings import APP_ID, AUDIENCE, VERSION
from utils.auth_bearer import JWTBearer

feed_router = APIRouter()


@feed_router.get("/feed", dependencies=[Depends(JWTBearer())])
async def info() -> str:
    return "200"


@feed_router.get("/search", dependencies=[Depends(JWTBearer())])
async def info() -> str:
    return "200"
