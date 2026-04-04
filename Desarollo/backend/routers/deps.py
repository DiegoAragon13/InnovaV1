# Dependencias compartidas entre routers
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from routers.auth import get_current_user
from models.user import User

bearer = HTTPBearer()

async def current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    db: AsyncSession = Depends(get_db)
) -> User:
    return await get_current_user(credentials.credentials, db)
