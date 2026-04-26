from pydantic import BaseModel

class DepositSchema(BaseModel):
    amount: float

class WithdrawSchema(BaseModel):
    amount: float

class TransferSchema(BaseModel):
    to_account: int
    amount: float