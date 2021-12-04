from datetime import datetime
import uuid
from services.db import DB
from settings import USER_ID


class AddFavoriteService():
    def __init__(self) -> None:
        ...

    async def __call__(self, startup_id: str):
        async def _favorite_exists(startup_id: str):
            query = f"""
                select exists (
                    select
                    from favorites
                    where user_id = $1
                    and startup_id = $2
                )
            """
            result = await DB.conn.fetchrow(query, startup_id, USER_ID)
            return result['exists']

        async def category_db():
            query = f"""
                insert into favorites (favorite_id, user_id, created_at, startup_id)
                VALUES($1, $2, $3, $4)
            """
            await DB.conn.execute(query, uuid.uuid4().hex, USER_ID, datetime.now(), uuid.UUID(startup_id))

        is_user_exists = await _favorite_exists(startup_id)
        if not is_user_exists:
            return await category_db()


add_favorite_service = AddFavoriteService()
