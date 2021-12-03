from datetime import datetime
import uuid
from services.db import DB
from settings import USER_ID


class AddFavoriteService():
    def __init__(self) -> None:
        ...

    async def __call__(self, startup_id: str):
        async def category_db():
            query = f"""
                insert into favorites (favorite_id, user_id, created_at, startup_id)
                VALUES($1, $2, $3, $4);
            """
            await DB.conn.fetch(query, uuid.uuid4().hex, USER_ID, datetime.now(), uuid.UUID(startup_id))

        return await category_db()


add_favorite_service = AddFavoriteService()
