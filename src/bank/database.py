from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base
import databases
import sqlalchemy as sa
from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///./blog.db"


database = databases.Database(DATABASE_URL)
metadata = sa.MetaData()

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

Base = declarative_base()

# Funções para conectar/desconectar (úteis no main.py)
async def startup():
    await database.connect()

async def shutdown():
    await database.disconnect()