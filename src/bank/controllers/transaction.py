from fastapi import APIRouter, Depends, HTTPException
from src.bank.schemas.transaction import DepositSchema, WithdrawSchema, TransferSchema
from src.bank.services.transaction import deposit
from src.bank.services.account import get_account_by_user
from src.bank.security import get_current_user

router = APIRouter(prefix="/transaction")

# 💰 depósito na conta
@router.post("/deposit")
async def deposit_money(data: DepositSchema, user=Depends(get_current_user)):
    account = await get_account_by_user(user['user_id'])

    if account != None:
        await deposit(account.id, data.amount)
        return {"message": "Depósito realizado"}
    else:
        raise HTTPException(status_code=404, detail="Account does not exists")

# 💸 quando sacar dinheiro da conta
@router.post("/withdraw")
async def withdraw_money(data: WithdrawSchema, user=Depends(get_current_user)):
    account = await get_account_by_user(user['user_id'])
    if not account:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    from src.bank.services.transaction import withdraw
    result = await withdraw(account.id, data.amount)
    return result

# 🔁 movimentação do dinheiro, fazer transferencia
@router.post("/transfer")
async def transfer_money(data: TransferSchema, user=Depends(get_current_user)):
    from_account = await get_account_by_user(user['user_id'])
    if not from_account:
        raise HTTPException(status_code=404, detail="Sua conta não foi encontrada")
    from src.bank.services.transaction import transfer
    result = await transfer(
        from_account_id=from_account.id,
        to_account_id=data.to_account_id,
        amount=data.amount
    )
    return result