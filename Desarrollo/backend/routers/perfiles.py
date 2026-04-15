from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from database import get_db
from models.perfil_voltaje import PerfilVoltaje
from models.user import User
from routers.deps import current_user

router = APIRouter(prefix="/perfiles", tags=["perfiles"])


class PerfilCreate(BaseModel):
    nombre: str
    voltaje_nominal: float
    voltaje_min: float
    voltaje_max: float
    corriente_max: float
    temperatura_max: float
    notas: Optional[str] = None


class PerfilOut(BaseModel):
    id: uuid.UUID
    nombre: str
    voltaje_nominal: float
    voltaje_min: float
    voltaje_max: float
    corriente_max: float
    temperatura_max: float
    notas: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}


@router.get("", response_model=list[PerfilOut])
async def listar(user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PerfilVoltaje).where(PerfilVoltaje.user_id == user.id))
    return result.scalars().all()


@router.post("", response_model=PerfilOut, status_code=201)
async def crear(data: PerfilCreate, user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    perfil = PerfilVoltaje(user_id=user.id, **data.model_dump())
    db.add(perfil)
    await db.commit()
    await db.refresh(perfil)
    return perfil


@router.put("/{id}", response_model=PerfilOut)
async def actualizar(id: uuid.UUID, data: PerfilCreate, user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PerfilVoltaje).where(PerfilVoltaje.id == id, PerfilVoltaje.user_id == user.id))
    perfil = result.scalar_one_or_none()
    if not perfil:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    for k, v in data.model_dump().items():
        setattr(perfil, k, v)
    await db.commit()
    await db.refresh(perfil)
    return perfil


@router.delete("/{id}", status_code=204)
async def eliminar(id: uuid.UUID, user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PerfilVoltaje).where(PerfilVoltaje.id == id, PerfilVoltaje.user_id == user.id))
    perfil = result.scalar_one_or_none()
    if not perfil:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    await db.delete(perfil)
    await db.commit()
