from pydantic import BaseModel
from datetime import datetime, timezone


class PostOut(BaseModel):
    id: int
    title: str
    content: str
    published_at: datetime

    class Config:
        from_attributes = True