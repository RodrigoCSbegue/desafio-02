from fastapi import FastAPI
from src.bank.controllers import auth, account, transaction
from src.bank.database import database, engine, metadata
from src.bank.controllers import history
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    metadata.create_all(engine)
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "http://127.0.0.1:5500/frontend",
    "http://localhost:5500/frontend",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(account.router)
app.include_router(transaction.router)
app.include_router(history.router)


@app.get("/")
async def root():
    return {"message": "API bancária rodando 🚀"}