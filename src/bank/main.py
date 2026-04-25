from fastapi import FastAPI
from src.bank.controllers import post
from src.bank.controllers import auth
from src.bank.database import database, engine, metadata
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    from src.bank.models.post import posts

    await database.connect()
    metadata.create_all(engine)
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(auth.router)
app.include_router(post.router)


@app.get("/")
async def root():
    return {"message": "API rodando 🚀"}