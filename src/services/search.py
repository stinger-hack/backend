class SearchService():
    def __init__(self) -> None:
        from services.db import DB
        self.DB = DB.conn

    async def __call__(self, search_str: str):
        async def search_db():
            await self.DB.fetch()

        return await search_db()


search_service = SearchService()
