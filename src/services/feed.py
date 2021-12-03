from services.db import DB
from pydantic.class_validators import validator
from pydantic import BaseModel
import uuid


class GetNewsDTO(BaseModel):
    news_id: uuid.UUID
    news_header: str
    news_text: str
    img_link: str

    @validator('news_id')
    def validate_id(news_id: uuid.UUID):
        return news_id.hex


class GetNewsService():
    def __init__(self) -> None:
        ...

    async def __call__(self):
        async def category_db():
            query = f"""
                select news_id, news_header, news_text, img_link
                from news
            """
            result = await DB.conn.fetch(query)

            return list(map(lambda row: GetNewsDTO(**row).dict(), result))

        return await category_db()


get_news_service = GetNewsService()
