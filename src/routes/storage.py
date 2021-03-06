from fastapi import APIRouter
from fastapi.datastructures import UploadFile
from fastapi.params import File
from fastapi.responses import FileResponse
storage_router = APIRouter()


@storage_router.get("/storage/{image_path}")
async def storage_categories(image_path: str):
    return FileResponse(image_path)

