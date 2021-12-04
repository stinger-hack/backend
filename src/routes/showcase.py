import pathlib
from fastapi import APIRouter
from fastapi.responses import UJSONResponse
from starlette.responses import FileResponse
from services.categories import categories_service
from services.showcase import showcase_service
from services.showcase_detailed import showcase_detailed_service
from services.my_showcase import my_showcase_service

showcase_router = APIRouter()


@showcase_router.get("/showcase")
async def showcase_categories() -> str:
    response = await categories_service()
    return UJSONResponse({'categories': response})

@showcase_router.get("/showcase/download")
async def showcase_categories() -> str:
    folder_path = pathlib.Path(__file__).parent.resolve().parent.resolve().parent.resolve()
    file_path = folder_path.joinpath(pathlib.Path(f"assets/voices.docx"))
    return FileResponse(file_path)


@showcase_router.get("/showcase/my")
async def showcase_categories() -> str:
    response = await my_showcase_service()
    return UJSONResponse({'showcase': response})


@showcase_router.get("/showcase/all")
async def showcase_categories() -> str:
    response = await showcase_service()
    return UJSONResponse({'showcase': response})


@showcase_router.get("/showcase/{main_category_slug}/{category_slug}")
async def showcase_subcategories(main_category_slug: str, category_slug: str) -> str:
    return await showcase_service(main_category_slug, category_slug)


@showcase_router.get("/showcase/{main_category_slug}/{category_slug}/{item_slug}")
async def showcase_detailed(main_category_slug: str, category_slug: str, item_slug: str) -> str:
    return await showcase_detailed_service(main_category_slug, category_slug, item_slug)
