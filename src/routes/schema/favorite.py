from pydantic import BaseModel


class FavoriteRequest(BaseModel):
    startup_id: str
