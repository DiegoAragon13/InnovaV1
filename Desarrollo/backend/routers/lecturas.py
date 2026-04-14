from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid
from datetime import datetime, timedelta

from database import get_db
from models.lectura import Lectura, LecturaHora, LecturaDia, LecturaMes, LecturaAnio
from models.user import User
from schemas.lectura import LecturaCreate, LecturaOut, LecturaAgregadaOut
from routers.deps import current_user
from services.alerta_service import evaluar_lectura

router = APIRouter(prefix="/lecturas", tags=["lecturas"])

@router.post("", response_model=LecturaOut, status_code=201)
async def recibir(data: LecturaCreate, db: AsyncSession = Depends(get_db)):
    lectura = Lectura(**data.model_dump())
    await evaluar_lectura(lectura, db)
    db.add(lectura)
    await db.commit()
    await db.refresh(lectura)
    return lectura

@router.get("/{dispositivo_id}", response_model=list[LecturaOut])
async def crudas(dispositivo_id: uuid.UUID, user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    desde = datetime.utcnow() - timedelta(hours=6)
    result = await db.execute(
        select(Lectura)
        .where(Lectura.dispositivo_id == dispositivo_id, Lectura.timestamp >= desde)
        .order_by(Lectura.timestamp.desc()).limit(500)
    )
    return result.scalars().all()

@router.get("/{dispositivo_id}/hora", response_model=list[LecturaAgregadaOut])
async def por_hora(dispositivo_id: uuid.UUID, user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(LecturaHora).where(LecturaHora.dispositivo_id == dispositivo_id)
        .order_by(LecturaHora.periodo_inicio.desc()).limit(168)
    )
    return result.scalars().all()

@router.get("/{dispositivo_id}/dia", response_model=list[LecturaAgregadaOut])
async def por_dia(dispositivo_id: uuid.UUID, user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(LecturaDia).where(LecturaDia.dispositivo_id == dispositivo_id)
        .order_by(LecturaDia.periodo_inicio.desc()).limit(90)
    )
    return result.scalars().all()

@router.get("/{dispositivo_id}/mes", response_model=list[LecturaAgregadaOut])
async def por_mes(dispositivo_id: uuid.UUID, user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(LecturaMes).where(LecturaMes.dispositivo_id == dispositivo_id)
        .order_by(LecturaMes.periodo_inicio.desc()).limit(24)
    )
    return result.scalars().all()

@router.get("/{dispositivo_id}/anio", response_model=list[LecturaAgregadaOut])
async def por_anio(dispositivo_id: uuid.UUID, user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(LecturaAnio).where(LecturaAnio.dispositivo_id == dispositivo_id)
        .order_by(LecturaAnio.periodo_inicio.desc())
    )
    return result.scalars().all()
