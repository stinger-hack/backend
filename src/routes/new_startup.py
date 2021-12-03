from fastapi import APIRouter
from fastapi.datastructures import UploadFile
from fastapi.params import File

new_startup_router = APIRouter()


@new_startup_router.post("/create_file")
async def image(image: UploadFile = File(...)):
    print(image.file)
    return {"filename": "new_image"}
