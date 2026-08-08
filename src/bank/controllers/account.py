from fastapi import APIRouter, Depends
from src.bank.services.account import get_account_by_user
from src.bank.security import get_current_user

router = APIRouter()

@router.get("/me")
async def get_my_account(user=Depends(get_current_user)):
    user_id = user.get("user_id")

    if not user_id:
        print("Conteúdo do user recebido:", user)
        raise HTTPException(status_code=400, detail="Não foi possível identificar o ID do usuário no Token.")

    account = await get_account_by_user(user_id)

    if not account:
        raise HTTPException(status_code=404, detail="Conta não encontrada para o usuário.")

    return account