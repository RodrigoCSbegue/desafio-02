from fastapi import APIRouter, Depends
from src.bank.database import database
from src.bank.models.transaction import transactions

router = APIRouter()

@router.get("/history/{user_id}")
async def get_history(user_id: int):
    query = transactions.select().where(
        transactions.c.user_id == user_id
    )

    result = await database.fetch_all(query)

    return result