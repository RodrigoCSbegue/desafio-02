from fastapi import Cookie, FastAPI, status, Header, APIRouter, Depends
from src.bank.database import database
from src.bank.schemas.post import PostIn, PostUpdate, PostUpdateIn
from src.bank.views.post import PostOut
from src.bank.models.post import posts
from src.bank.services.post import PostService
from src.bank.database import database   # ← use Depends se estiver usando Session
from sqlalchemy.ext.asyncio import AsyncSession
from src.bank.security import get_current_user

router = APIRouter(prefix = "/posts")

service = PostService()

@router.get("/", response_model = list [PostOut])
async def read_posts(published: bool, limit: int, skip: int = 0):
    return await service.read_all(published = published, limit = limit, skip = skip)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostOut)
async def create_post(post: PostIn, user = Depends(get_current_user)):
    created_id = await service.create(post)
    new_post = await service.read(created_id)
    return new_post

@router.get("/{id}", response_model = PostOut)
async def read_post(id: int):
    return await service.read(id)


@router.patch("/{id}", response_model = PostOut)
async def update_post(id: int, post: PostUpdateIn):
    return await service.update(id, post)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, response_model = None)
async def delete_post(id: int):
    await service.delete(id)
