from pydantic import BaseModel, EmailStr

class RegistroSchema(BaseModel):
    email: EmailStr
    password: str
    nombre: str

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshSchema(BaseModel):
    refresh_token: str
