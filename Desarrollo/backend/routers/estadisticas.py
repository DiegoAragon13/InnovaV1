from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
import uuid
from pydantic import BaseModel
from typing import Optional

from database import get_db
from models.lectura import Lectura
from models.alerta import Alerta
from models.user import User
from routers.deps import current_user

router = APIRouter(prefix="/estadisticas", tags=["estadisticas"])


class EstadisticasOut(BaseModel):
    voltaje_avg: Optional[float]
    voltaje_min: Optional[float]
    voltaje_max: Optional[float]
    corriente_avg: Optional[float]
    corriente_min: Optional[float]
    corriente_max: Optional[float]
    temperatura_avg: Optional[float]
    temperatura_min: Optional[float]
    temperatura_max: Optional[float]
    vibracion_avg: Optional[float]
    vibracion_max: Optional[float]
    total_lecturas: int
    total_alertas: int
    alertas_criticas: int


@router.get("/{dispositivo_id}", response_model=EstadisticasOut)
async def resumen(
    dispositivo_id: uuid.UUID,
    user: User = Depends(current_user),
    db: AsyncSession = Depends(get_db)
):
    # Agregados de lecturas
    result = await db.execute(
        select(
            func.avg(Lectura.voltaje).label("voltaje_avg"),
            func.min(Lectura.voltaje).label("voltaje_min"),
            func.max(Lectura.voltaje).label("voltaje_max"),
            func.avg(Lectura.corriente).label("corriente_avg"),
            func.min(Lectura.corriente).label("corriente_min"),
            func.max(Lectura.corriente).label("corriente_max"),
            func.avg(Lectura.temperatura).label("temperatura_avg"),
            func.min(Lectura.temperatura).label("temperatura_min"),
            func.max(Lectura.temperatura).label("temperatura_max"),
            func.avg(Lectura.vibracion).label("vibracion_avg"),
            func.max(Lectura.vibracion).label("vibracion_max"),
            func.count(Lectura.id).label("total_lecturas"),
        ).where(Lectura.dispositivo_id == dispositivo_id)
    )
    row = result.one()

    # Conteo de alertas
    total_alertas = await db.scalar(
        select(func.count(Alerta.id)).where(Alerta.dispositivo_id == dispositivo_id)
    )
    alertas_criticas = await db.scalar(
        select(func.count(Alerta.id)).where(
            Alerta.dispositivo_id == dispositivo_id,
            Alerta.severidad == "critico"
        )
    )

    return EstadisticasOut(
        voltaje_avg=row.voltaje_avg,
        voltaje_min=row.voltaje_min,
        voltaje_max=row.voltaje_max,
        corriente_avg=row.corriente_avg,
        corriente_min=row.corriente_min,
        corriente_max=row.corriente_max,
        temperatura_avg=row.temperatura_avg,
        temperatura_min=row.temperatura_min,
        temperatura_max=row.temperatura_max,
        vibracion_avg=row.vibracion_avg,
        vibracion_max=row.vibracion_max,
        total_lecturas=row.total_lecturas or 0,
        total_alertas=total_alertas or 0,
        alertas_criticas=alertas_criticas or 0,
    )
