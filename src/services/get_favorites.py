import uuid
from pydantic import BaseModel
from pydantic.class_validators import validator
from services.db import DB
from settings import USER_ID
from datetime import datetime

class GetFavoritesDTO(BaseModel):
    startup_id: uuid.UUID
    project_name: str
    description: str
    presentation_link: str
    stage: str
    study_facility: str
    user_id: uuid.UUID
    category_name: str
    img_link: str
    slug: str
    created_at: datetime

    @validator('startup_id', 'user_id')
    def validate_id(startup_id: uuid.UUID):
        return startup_id.hex

    @validator('created_at')
    def validate_date(created_at: datetime):
        return created_at.isoformat()


class GetFavoritesService():
    def __init__(self) -> None:
        ...

    async def __call__(self):
        async def category_db():
            query = f"""
                select s.startup_id, s.project_name, s.description, s.presentation_link, s.created_at,
	                s.stage, s.study_facility, s.user_id, sc.category_name, s.img_link, s.slug
                from public.startup s
                join startup_categories sc 
                on s.category_id = sc.category_id
                join favorites f
                on f.startup_id = s.startup_id
                where f.user_id = '{USER_ID}'
            """
            result = await DB.conn.fetch(query)

            return list(map(lambda row: GetFavoritesDTO(**row).dict(), result))

        return await category_db()


get_favorites_service = GetFavoritesService()
