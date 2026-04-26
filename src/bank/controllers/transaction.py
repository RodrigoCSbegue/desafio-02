from fastapi import APIRouter, Depends
from src.bank.schemas.transaction import DepositSchema
from src.bank.services.transaction import deposit
from src.bank.services.account import get_account_by_user
from src.bank.security import get_current_user

router = APIRouter(prefix="/transaction")

@router.post("/deposit")
async def deposit_money(data: DepositSchema, user=Depends(get_current_user)):
    account = await get_account_by_user(user.id)
    await deposit(account.id, data.amount)
    return {"message": "Depósito realizado"}