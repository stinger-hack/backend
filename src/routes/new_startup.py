from fastapi import APIRouter
from fastapi.datastructures import UploadFile
from fastapi.params import File

new_startup_router = APIRouter()


@new_startup_router.post("/create_file")
async def image(upload_file: UploadFile = File(...)):

    return {"msg": "file upload successul"}
