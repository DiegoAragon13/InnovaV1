from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt, JWTError
import uuid

from database import get_db
from config import settings
from models.user import User
from models.sesion import Sesion
from schemas.auth import RegistroSchema, LoginSchema, TokenSchema, RefreshSchema

router = APIRouter(prefix="/auth", tags=["auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(user_id: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({"sub": user_id, "exp": expire}, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def create_refresh_token() -> str:
    return str(uuid.uuid4())

async def get_current_user(token: str, db: AsyncSession) -> User:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    result = await db.execute(select(User).where(User.id == uuid.UUID(user_id)))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado")
    return user

@router.post("/registro", response_model=TokenSchema, status_code=201)
async def registro(data: RegistroSchema, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == data.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email ya registrado")
    user = User(email=data.email, password_hash=hash_password(data.password), nombre=data.nombre)
    db.add(user)
    await db.flush()
    refresh = create_refresh_token()
    sesion = Sesion(
        user_id=user.id,
        refresh_token=refresh,
        expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    db.add(sesion)
    await db.commit()
    return TokenSchema(access_token=create_access_token(str(user.id)), refresh_token=refresh)

@router.post("/login", response_model=TokenSchema)
async def login(data: LoginSchema, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    refresh = create_refresh_token()
    sesion = Sesion(
        user_id=user.id,
        refresh_token=refresh,
        expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    db.add(sesion)
    await db.commit()
    return TokenSchema(access_token=create_access_token(str(user.id)), refresh_token=refresh)

@router.post("/refresh", response_model=TokenSchema)
async def refresh(data: RefreshSchema, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Sesion).where(Sesion.refresh_token == data.refresh_token, Sesion.revocado == False))
    sesion = result.scalar_one_or_none()
    if not sesion or sesion.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Refresh token inválido o expirado")
    sesion.revocado = True
    new_refresh = create_refresh_token()
    nueva_sesion = Sesion(
        user_id=sesion.user_id,
        refresh_token=new_refresh,
        expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    db.add(nueva_sesion)
    await db.commit()
    return TokenSchema(access_token=create_access_token(str(sesion.user_id)), refresh_token=new_refresh)

@router.post("/logout")
async def logout(data: RefreshSchema, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Sesion).where(Sesion.refresh_token == data.refresh_token))
    sesion = result.scalar_one_or_none()
    if sesion:
        sesion.revocado = True
        await db.commit()
    return {"detail": "Sesión cerrada"}
