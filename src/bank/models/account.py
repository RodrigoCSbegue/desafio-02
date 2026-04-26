from sqlalchemy import Table, Column, Integer, ForeignKey, Float
from src.bank.database import metadata

# Tabela do conta
accounts = Table(
    "accounts",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("content", Float, default=0.0),
    Column("balance", Float, default=0.0),
)
