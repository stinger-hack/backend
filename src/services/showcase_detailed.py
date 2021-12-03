from typing import Optional
import uuid
from pydantic import BaseModel
from pydantic.class_validators import validator
from services.db import DB


class ShowcaseDetailedDTO(BaseModel):
    startup_id: uuid.UUID
    project_name: str
    description: str
    presentation_link: str
    stage: str
    study_facility: str
    user_id: uuid.UUID
    category_name: str

    @validator('startup_id', 'user_id')
    def validate_id(startup_id: uuid.UUID):
        return startup_id.hex


class ShowcaseDetailedService():
    def __init__(self) -> None:
        ...

    async def __call__(self, main_category_slug: str, category_slug: str, item_slug: str):
        async def category_db():
            query = f"""
                select startup_id, project_name, description, presentation_link, 
	                stage, study_facility, user_id, sc.category_name, 
                    sc_main.category_name as main_category_name
                from public.startup s
                join startup_categories sc 
                on s.category_id = sc.category_id
                join startup_categories sc_main
                on sc.parent_id = sc_main.category_id
                where sc.slug = '{category_slug}'
                and s.slug = '{item_slug}'
                and sc_main.parent_id is null
                and sc_main.slug = '{main_category_slug}'
            """
            result = await DB.conn.fetch(query)

            return list(map(lambda row: ShowcaseDetailedDTO(**row).dict(), result))

        return await category_db()


showcase_detailed_service = ShowcaseDetailedService()
