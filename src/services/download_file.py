
import pathlib

from starlette.datastructures import UploadFile


class DownloadFileService():

    async def __call__(self, uploaded_file: UploadFile):
        async def download_file_storage(uploaded_file: UploadFile):
            folder_path = pathlib.Path(__file__).parent.resolve().parent.resolve().parent.resolve()
            word_path = folder_path.joinpath(pathlib.Path(f"assets/{uploaded_file.filename}"))
            with open(word_path, "wb+") as file_object:
                file_object.write(uploaded_file.file.read())
            return uploaded_file.filename

        return await download_file_storage(uploaded_file)


download_file_service = DownloadFileService()
