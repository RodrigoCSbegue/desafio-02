from pydantic import BaseModel, EmailStr

# 📥 Cadastro
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


# 📥 Login
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# 📤 Token de resposta
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# 📤 Dados do usuário sem senha
class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True