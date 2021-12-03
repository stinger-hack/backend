import uuid
from datetime import datetime
from pydantic import BaseModel, validator

from services.db import DB

class SearchServiceDTO(BaseModel):
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

class SearchService:
    def __init__(self) -> None:
        ...

    async def __call__(self, search_str: str):
        async def search_db(search_str: str):
            query = f"""
                select
                    startup_id, project_name, description, presentation_link, s.created_at,
	                stage, study_facility, user_id, sc.category_name, img_link, s.slug
                from startup s
                join startup_categories sc 
                on s.category_id = sc.category_id 
                where s.project_name ilike '%{search_str}%'
                order by s.created_at 
            """
            return await DB.conn.fetch(query)
        result = await search_db(search_str)
        return list(map(lambda row: SearchServiceDTO(**row).dict(), result))


search_service = SearchService()
