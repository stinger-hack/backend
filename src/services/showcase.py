from typing import Optional
from datetime import datetime
import uuid
from pydantic import BaseModel
from pydantic.class_validators import validator
from services.db import DB


class ShowcaseDTO(BaseModel):
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


class ShowcaseService():
    def __init__(self) -> None:
        ...

    async def __call__(self, category_slug: Optional[str] = None, main_category_slug: Optional[str] = None):
        async def category_db():
            query = """
                select startup_id, project_name, description, presentation_link, s.created_at,
	                stage, study_facility, user_id, sc.category_name, img_link, s.slug
                from public.startup s
                join startup_categories sc 
                on s.category_id = sc.category_id
            """
            if category_slug and main_category_slug:
                ''.join((query, f" where s.category_slug = '{category_slug}'"))
            result = await DB.conn.fetch(query)

            return list(map(lambda row: ShowcaseDTO(**row).dict(), result))

        return await category_db()


showcase_service = ShowcaseService()
