from sqlalchemy import Table, Column, Integer, String, Float
from src.bank.database import metadata

# Tabela de usuarios
users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("email", String, unique=True, nullable=False),
    Column("password", String, nullable=False),
    Column("balance", Float, default=0.0),
)