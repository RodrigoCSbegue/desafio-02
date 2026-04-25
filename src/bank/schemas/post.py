from datetime import datetime
from pydantic import BaseModel, ConfigDict


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = False
    published_at: datetime | None = None


# Para criar post (sem id)
class PostIn(PostBase):
    pass


# Para retornar post (com id)
class Post(PostBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# Para atualizar post (todos campos opcionais)
class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    published: bool | None = None
    published_at: datetime | None = None


# Alias para Update (caso você queira usar esse nome)
class PostUpdateIn(PostUpdate):
    pass