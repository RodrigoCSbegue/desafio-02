from fastapi import APIRouter, Depends
from src.bank.database import database
from src.bank.models.transaction import transactions

router = APIRouter()

# Ver o historico de movimentação da conta
@router.get("/history/{account_id}")
async def get_history(account_id: int):
    query = transactions.select().where(
        (transactions.c.from_account == account_id) |
        (transactions.c.to_account == account_id)
    )
    result = await database.fetch_all(query)
    return result