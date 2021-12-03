
from services.db import DB


class GetFavoritesService():

    async def __call__(self, p):
        async def category_db():
            query = f"""
                insert into public.startup
                (startup_id, project_name, description, presentation_link, stage, 
                    study_facility, user_id, category_id, slug, img_link, created_at)
                values (?, '', '', '', '', '', ?, ?, '', '', '');
            """
            await DB.conn.fetch(query, )

        return await category_db()


get_favorites_service = GetFavoritesService()
