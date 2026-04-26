from fastapi import HTTPException
from src.bank.database import database
from src.bank.models.account import accounts
from src.bank.models.transaction import transactions


# 💰 DEPÓSITO
async def deposit(account_id: int, amount: float):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Valor inválido")

    async with database.transaction():
        # atualiza saldo
        await database.execute(
            accounts.update()
            .where(accounts.c.id == account_id)
            .values(balance=accounts.c.balance + amount)
        )

        # registra transação
        await database.execute(
            transactions.insert().values(
                type="deposit",
                amount=amount,
                from_account=account_id
            )
        )

    return {"message": "Depósito realizado com sucesso"}


# 💸 SAQUE
async def withdraw(account_id: int, amount: float):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Valor inválido")

    account = await database.fetch_one(
        accounts.select().where(accounts.c.id == account_id)
    )

    if not account:
        raise HTTPException(status_code=404, detail="Conta não encontrada")

    if account.balance < amount:
        raise HTTPException(status_code=400, detail="Saldo insuficiente")

    async with database.transaction():
        # atualiza saldo
        await database.execute(
            accounts.update()
            .where(accounts.c.id == account_id)
            .values(balance=accounts.c.balance - amount)
        )

        # registra transação
        await database.execute(
            transactions.insert().values(
                type="withdraw",
                amount=amount,
                from_account=account_id
            )
        )

    return {"message": "Saque realizado com sucesso"}


# 🔁 TRANSFERÊNCIA
async def transfer(from_account_id: int, to_account_id: int, amount: float):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Valor inválido")

    if from_account_id == to_account_id:
        raise HTTPException(status_code=400, detail="Não pode transferir para si mesmo")

    from_account = await database.fetch_one(
        accounts.select().where(accounts.c.id == from_account_id)
    )

    to_account = await database.fetch_one(
        accounts.select().where(accounts.c.id == to_account_id)
    )

    if not from_account or not to_account:
        raise HTTPException(status_code=404, detail="Conta não encontrada")

    if from_account.balance < amount:
        raise HTTPException(status_code=400, detail="Saldo insuficiente")

    async with database.transaction():
        # debita
        await database.execute(
            accounts.update()
            .where(accounts.c.id == from_account_id)
            .values(balance=accounts.c.balance - amount)
        )

        # credita
        await database.execute(
            accounts.update()
            .where(accounts.c.id == to_account_id)
            .values(balance=accounts.c.balance + amount)
        )

        # registra transação
        await database.execute(
            transactions.insert().values(
                type="transfer",
                amount=amount,
                from_account=from_account_id,
                to_account=to_account_id
            )
        )

    return {"message": "Transferência realizada com sucesso"}


# 📊 HISTÓRICO
async def get_transaction_history(account_id: int):
    query = transactions.select().where(
        (transactions.c.from_account == account_id) |
        (transactions.c.to_account == account_id)
    )

    results = await database.fetch_all(query)

    return results