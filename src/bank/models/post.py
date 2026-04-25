import sqlalchemy as sa
from datetime import datetime
from src.bank.database import metadata


posts = sa.Table(
    "posts",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
    sa.Column("title", sa.String(150), nullable=False),        # unique removido
    sa.Column("content", sa.Text, nullable=False),
    sa.Column("published_at", sa.TIMESTAMP(timezone=True), nullable=True),
    sa.Column("published", sa.Boolean, default=False, nullable=False),
)
