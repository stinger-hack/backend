import uuid
from pydantic import BaseModel
from pydantic.class_validators import validator
from services.db import DB


class CategoryDTO(BaseModel):
    category_id: uuid.UUID
    slug: str
    main_slug: str
    category_name: str
    main_category_name: str

    @validator('category_id')
    def validate_id(category_id: uuid.UUID):
        return category_id.hex


class CategoriesService():
    def __init__(self) -> None:
        ...

    async def __call__(self):
        async def category_db():
            query = """
                select pc.category_id,
                pc_main.slug as main_slug, pc.slug, 
                pc.category_name as main_category_name, pc_main.category_name 
                from startup_categories pc
                join startup_categories pc_main 
                on pc.parent_id = pc_main.category_id 
                where pc_main.parent_id is null
            """
            result = await DB.conn.fetch(query)

            valid_result = list(map(lambda row: CategoryDTO(**row).dict(), result))

            result_json = {}

            for item in valid_result:
                subcategory = {
                    'slug': item['slug'],
                    'category_id': item['category_id'],
                    'main_category_name': item['main_category_name'],
                    'category_name': item['category_name'],
                }
                result_json[item['main_slug']] = subcategory

            return result_json

        return await category_db()


categories_service = CategoriesService()
