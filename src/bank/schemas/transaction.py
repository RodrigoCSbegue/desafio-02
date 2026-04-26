from pydantic import BaseModel

# 💰 Deposito
class DepositSchema(BaseModel):
    amount: float

# 💸 Saque
class WithdrawSchema(BaseModel):
    amount: float

# 🔁 Transferencia
class TransferSchema(BaseModel):
    to_account_id: int
    amount: float