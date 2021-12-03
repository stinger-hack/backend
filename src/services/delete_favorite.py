from services.db import DB
from settings import USER_ID


class DeleteFavoriteService():
    def __init__(self) -> None:
        ...

    async def __call__(self, startup_id: str):
        async def delete_favorite_db():
            query = f"""
                delete from favorites
                where user_id = $1
                and startup_id = $2
            """
            await DB.conn.fetch(query,USER_ID, startup_id)

        return await delete_favorite_db()


delete_favorite_service = DeleteFavoriteService()
