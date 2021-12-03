from fastapi import APIRouter
from fastapi.datastructures import UploadFile
from fastapi.params import File
from services.download_file import download_file_service

from utils.docx_parser import my_docx_parser_service

new_startup_router = APIRouter()


@new_startup_router.post("/create_file")
async def image(upload_file: UploadFile = File(...)):
    file_path = await download_file_service(upload_file)
    result = await my_docx_parser_service(file_path)
    await new_startup_service(result)
    return result
