from fastapi import APIRouter
from services.search import search_service
from services.feed import get_news_service

feed_router = APIRouter()


@feed_router.get("/feed")
async def info() -> str:
    return await get_news_service()


@feed_router.get("/search")
async def info(search_str: str) -> str:
    return await search_service(search_str)
