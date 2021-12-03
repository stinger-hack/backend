import uuid
from datetime import datetime
from services.db import DB
from slugify import slugify

class InsertShowcaseService():

    async def __call__(self, showcase: dict):

        async def get_user_id(email: str):
            query = f"""
                select user_id
                from users
                where email = $1
            """
            result = await DB.conn.fetchrow(query, email)
            return result['user_id']

        async def insert_startup(showcase: dict):
            user_id = await get_user_id(showcase['email'])
            query = f"""
                insert into startup
                    (startup_id, project_name, description, stage, 
                    study_facility, user_id, category_id, slug, img_link, created_at)
                values ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11);
            """
            await DB.conn.fetch(query, uuid.uuid4(), showcase['project_name'], showcase['description'], showcase['stage'],
                                'None', user_id, slugify(showcase['project_name']), 'https://stinger-hack.ru/storage/showcase_2.png', datetime.now())

        return await insert_startup(showcase)


insert_showcase_service = InsertShowcaseService()
