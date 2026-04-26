from sqlalchemy import Table, Column, Integer, String, Float, ForeignKey
from src.bank.database import metadata

# Tabela do historico da conta
transactions = Table(
    "transactions",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("type", String),  # deposit | withdraw
    Column("amount", Float),
)