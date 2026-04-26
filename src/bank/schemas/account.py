from pydantic import BaseModel

# 📥 Conta
class AccountResponse(BaseModel):
    id: int
    balance: float