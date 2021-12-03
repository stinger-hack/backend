from fastapi import APIRouter
from fastapi.responses import FileResponse
storage_router = APIRouter()
import pathlib
cur_path = pathlib.Path(__file__).parent.resolve()


@storage_router.get("/storage/{image_name}")
async def storage_categories(image_name: str):
    image_path = cur_path.joinpath(pathlib.Path(f'assets/{image_name}'))

    return FileResponse(image_path)