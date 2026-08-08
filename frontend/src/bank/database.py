import databases
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

DATABASE_URL = "sqlite:///./bank.db"

database = databases.Database(DATABASE_URL)
metadata = sa.MetaData()

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

Base = declarative_base()

# Funções para conectar/desconectar que esta no main.py
async def startup():
    await database.connect()

async def shutdown():
    await database.disconnect()