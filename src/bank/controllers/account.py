from fastapi import APIRouter, Depends
from src.bank.services.account import get_account_by_user
from src.bank.security import get_current_user

router = APIRouter()

@router.get("/me")
async def get_my_account(user=Depends(get_current_user)):
    account = await get_account_by_user(user.id)
    return account