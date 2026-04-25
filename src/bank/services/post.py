from fastapi import HTTPException, status
from src.bank.database import database
from src.bank.models.post import posts
from src.bank.schemas.post import PostIn, PostUpdateIn
from typing import Any, Dict


class PostService:

    async def read_all(
        self,
        published: bool | None = None,
        limit: int = 10,
        skip: int = 0
    ) -> list[Dict]:
        query = posts.select()

        if published is not None:
            query = query.where(posts.c.published == published)

        query = query.limit(limit).offset(skip)
        return await database.fetch_all(query)

    async def create(self, post: PostIn) -> int:
        command = posts.insert().values(
            title=post.title,
            content=post.content,
            published_at=post.published_at,
            published=post.published,
        )
        return await database.execute(command)

    async def read(self, id: int):
        post = await self.__get_by_id(id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        return post

    async def update(self, id: int, post: PostUpdateIn):
        existing = await self.__get_by_id(id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found"
            )

        data = post.model_dump(exclude_unset=True)

        if data:
            command = posts.update().where(posts.c.id == id).values(**data)
            await database.execute(command)

        return await self.__get_by_id(id)

    async def delete(self, id: int):
        command = posts.delete().where(posts.c.id == id)
        await database.execute(command)

    async def __get_by_id(self, id: int):
        query = posts.select().where(posts.c.id == id)
        return await database.fetch_one(query)


post_service = PostService()