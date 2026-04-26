from src.bank.database import database
from src.bank.models.user import users
from src.bank.models.account import accounts
from src.bank.security import verify_password, sign_jwt


async def authenticate_user(data):
    query = users.select().where(users.c.email == data.email)
    user = await database.fetch_one(query)

    if not user:
        return None

    if not verify_password(data.password, user.password):
        return None

    return sign_jwt(user_id=user.id)
