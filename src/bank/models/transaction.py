from sqlalchemy import Table, Column, Integer, Float, String, DateTime
from datetime import datetime
from src.bank.database import metadata

# Tabela de transferencias
transactions = Table(
    "transactions",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("type", String),
    Column("amount", Float),
    Column("from_account", Integer),
    Column("to_account", Integer, nullable=True),
    Column("created_at", DateTime, default=datetime.utcnow),
)