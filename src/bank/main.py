from fastapi import FastAPI
from src.bank.controllers import auth, account, transaction
from src.bank.database import database, engine, metadata
from src.bank.controllers import history
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    metadata.create_all(engine)
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(account.router)
app.include_router(transaction.router)
app.include_router(history.router)


@app.get("/")
async def root():
    return {"message": "API bancária rodando 🚀"}