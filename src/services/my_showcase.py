from typing import Optional
from datetime import datetime
import uuid
from pydantic import BaseModel
from pydantic.class_validators import validator
from services.db import DB
from settings import USER_ID

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
    is_liked: Optional[uuid.UUID]

    @validator('startup_id', 'user_id')
    def validate_id(startup_id: uuid.UUID):
        return startup_id.hex

    @validator('created_at')
    def validate_date(created_at: datetime):
        return created_at.isoformat()

    @validator('is_liked')
    def validate_is_liked(is_liked: str):
        return True if is_liked else False


class MyShowcaseService():
    def __init__(self) -> None:
        ...

    async def __call__(self, category_slug: Optional[str] = None, main_category_slug: Optional[str] = None):
        async def category_db():
            query = """
                select s.startup_id, s.project_name, s.description, s.presentation_link, s.created_at,
	                s.stage, s.study_facility, s.user_id, sc.category_name, s.img_link, s.slug, 
	                f.favorite_id as is_liked
                from public.startup s
                join startup_categories sc 
                on s.category_id = sc.category_id
                left join favorites f
                on f.startup_id = s.startup_id
            """
            if category_slug and main_category_slug:
                ''.join((query, f" where s.category_slug = '{category_slug}' and s.user_id = '{USER_ID}'"))
            else:
                 ''.join((query, f" where s.user_id = '{USER_ID}'"))
            result = await DB.conn.fetch(query)

            return list(map(lambda row: ShowcaseDTO(**row).dict(), result))

        return await category_db()


my_showcase_service = MyShowcaseService()
