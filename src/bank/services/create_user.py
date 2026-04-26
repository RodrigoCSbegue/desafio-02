from fastapi import HTTPException
from src.bank.database import database
from src.bank.models.user import users
from src.bank.models.account import accounts
from src.bank.security import hash_password
from src.bank.schemas.auth import UserCreate


async def create_user(data: UserCreate):
    # 🔍 verifica se já existe usuário com esse email
    existing = await database.fetch_one(
        users.select().where(users.c.email == data.email)
    )

    if existing:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    # 🔐 hash da senha
    hashed_password = hash_password(data.password)

    # 👤 cria usuário
    query = users.insert().values(
        name=data.name,
        email=data.email,
        password=hashed_password
    )

    user_id = await database.execute(query)

    # 🏦 cria conta automaticamente
    await database.execute(
        accounts.insert().values(user_id=user_id, balance=0)
    )

    return {
        "id": user_id,
        "message": "Usuário criado com sucesso"
    }