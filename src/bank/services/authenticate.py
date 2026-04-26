from src.bank.database import database
from src.bank.models.user import users
from src.bank.security import verify_password, sign_jwt
from src.bank.schemas.auth import UserLogin


async def authenticate_user(data: UserLogin):
    # 🔍 busca usuário pelo email
    query = users.select().where(users.c.email == data.email)
    user = await database.fetch_one(query)

    # ❌ usuário não existe
    if not user:
        return None

    # 🔐 verifica senha
    if not verify_password(data.password, user.password):
        return None

    # 🎟️ gera token
    return sign_jwt(user_id=user.id)