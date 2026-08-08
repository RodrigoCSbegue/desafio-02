from src.bank.database import database
from src.bank.models.account import accounts

# 🔍 busca usuário pelo usuario
async def get_account_by_user(user_id: int):
    query = accounts.select().where(accounts.c.user_id == user_id)
    return await database.fetch_one(query)