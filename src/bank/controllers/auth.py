from fastapi import APIRouter, HTTPException
from src.bank.schemas.auth import UserCreate, UserLogin, Token
from src.bank.services.create_user import create_user
from src.bank.services.authenticate import authenticate_user

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/register")
async def register(data: UserCreate):
    user = await create_user(data)
    return user


@router.post("/login", response_model=Token)
async def login(data: UserLogin):
    token = await authenticate_user(data)

    if not token:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    return token