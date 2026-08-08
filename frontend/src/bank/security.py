import time
from uuid import uuid4
import hashlib

import jwt
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer

SECRET = "5dfbbabc-1061-4096-9622-bb7049c758e0"
ALGORITHM = "HS256"
AUDIENCE = "bank-171"

# hash da senha
def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()

# verificação da senha
def verify_password(plain_password: str, hashed_password: str):
    return hash_password(plain_password) == hashed_password


def sign_jwt(user_id: int):
    now = time.time()
    payload = {
        "iss": "bank-171.com.br",
        "user_id": str(user_id),
        "aud": AUDIENCE,
        "exp": now + (60 * 60), # 60 minutos
        "iat": now,
        "nbf": now,
        "jti": uuid4().hex,
    }

    token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)

    return {
        "access_token": token,
        "token_type": "bearer"
    }


async def decode_jwt(token: str):
    try:
        return jwt.decode(token, SECRET, algorithms=[ALGORITHM], audience=AUDIENCE)
    except Exception:
        return None


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        authorization = request.headers.get("Authorization", "")
        scheme, _, credentials = authorization.partition(" ")

        if scheme != "Bearer" or not credentials:
            raise HTTPException(status_code=401, detail="Token inválido")

        payload = await decode_jwt(credentials)

        if not payload:
            raise HTTPException(status_code=401, detail="Token inválido ou expirado")

        return payload


async def get_current_user(token=Depends(JWTBearer())):
    return {"user_id": token["user_id"]}