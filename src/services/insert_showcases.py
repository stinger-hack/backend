import enum
import uuid
from datetime import datetime
from services.db import DB
from slugify import slugify

class InsertShowcaseService():

    async def __call__(self, showcase: dict):

        def get_stage(stage: str):
            enum_stage = {
                'Прототип': 'prototype'
            }
            return enum_stage[stage]

        async def get_user_id(email: str):
            query = f"""
                select user_id
                from users
                where email = $1
            """
            result = await DB.conn.fetchrow(query, email)
            return result['user_id'] if result else None

        async def insert_startup(showcase: dict):
            user_id = await get_user_id(showcase['email'].strip())
            stage = get_stage(showcase['stage'])
            query = f"""
                insert into startup
                    (startup_id, project_name, description, stage, study_facility,
                     user_id, slug, img_link, created_at)
                values 
                    ($1, $2, $3, $4::project_stage, $5, $6, $7, $8, $9);
            """
            await DB.conn.fetch(query, uuid.uuid4(), showcase['project_name'], showcase['description'], stage, 'None', 
            user_id, slugify(showcase['project_name']), 'https://stinger-hack.ru/storage/showcase_2.png', datetime.now())

        return await insert_startup(showcase)


insert_showcase_service = InsertShowcaseService()
