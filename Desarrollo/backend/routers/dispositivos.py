from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid

from database import get_db
from models.dispositivo import Dispositivo
from models.user import User
from schemas.dispositivo import DispositivoCreate, DispositivoUpdate, DispositivoOut
from routers.deps import current_user

router = APIRouter(prefix="/dispositivos", tags=["dispositivos"])

@router.get("", response_model=list[DispositivoOut])
async def listar(user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Dispositivo).where(Dispositivo.user_id == user.id))
    return result.scalars().all()

@router.post("", response_model=DispositivoOut, status_code=201)
async def crear(data: DispositivoCreate, user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    dispositivo = Dispositivo(user_id=user.id, nombre=data.nombre, ble_mac_address=data.ble_mac_address)
    db.add(dispositivo)
    await db.commit()
    await db.refresh(dispositivo)
    return dispositivo

@router.put("/{id}", response_model=DispositivoOut)
async def actualizar(id: uuid.UUID, data: DispositivoUpdate, user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Dispositivo).where(Dispositivo.id == id, Dispositivo.user_id == user.id))
    dispositivo = result.scalar_one_or_none()
    if not dispositivo:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    dispositivo.nombre = data.nombre
    await db.commit()
    await db.refresh(dispositivo)
    return dispositivo

@router.delete("/{id}", status_code=204)
async def eliminar(id: uuid.UUID, user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Dispositivo).where(Dispositivo.id == id, Dispositivo.user_id == user.id))
    dispositivo = result.scalar_one_or_none()
    if not dispositivo:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    await db.delete(dispositivo)
    await db.commit()
