from fastapi import APIRouter
from src.bank.schemas.auth import LoginIn
from src.bank.security import sign_jwt
from src.bank.views.auth import LoginOut

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/login", response_model = LoginOut)
async def login(data: LoginIn):
    return sign_jwt(user_id = data.user_id)