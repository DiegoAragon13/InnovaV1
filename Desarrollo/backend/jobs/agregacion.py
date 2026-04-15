from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
import uuid

from database import AsyncSessionLocal
from models.lectura import Lectura, LecturaHora, LecturaDia, LecturaMes, LecturaAnio
from models.dispositivo import Dispositivo


async def _agregar(modelo_origen, modelo_destino, desde: datetime, hasta: datetime):
    async with AsyncSessionLocal() as db:
        # Obtener todos los dispositivos
        dispositivos = (await db.execute(select(Dispositivo.id))).scalars().all()

        for disp_id in dispositivos:
            result = await db.execute(
                select(
                    func.avg(modelo_origen.voltaje).label("voltaje_avg"),
                    func.min(modelo_origen.voltaje).label("voltaje_min"),
                    func.max(modelo_origen.voltaje).label("voltaje_max"),
                    func.avg(modelo_origen.corriente).label("corriente_avg"),
                    func.min(modelo_origen.corriente).label("corriente_min"),
                    func.max(modelo_origen.corriente).label("corriente_max"),
                    func.avg(modelo_origen.temperatura).label("temperatura_avg"),
                    func.min(modelo_origen.temperatura).label("temperatura_min"),
                    func.max(modelo_origen.temperatura).label("temperatura_max"),
                    func.avg(modelo_origen.vibracion).label("vibracion_avg"),
                    func.max(modelo_origen.vibracion).label("vibracion_max"),
                ).where(
                    modelo_origen.dispositivo_id == disp_id,
                    modelo_origen.timestamp >= desde,
                    modelo_origen.timestamp < hasta,
                )
            )
            row = result.one()

            if row.voltaje_avg is None:
                continue

            agregado = modelo_destino(
                dispositivo_id=disp_id,
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
                periodo_inicio=desde,
            )
            db.add(agregado)

        await db.commit()


async def job_agregar_hora():
    ahora = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
    desde = ahora - timedelta(hours=1)
    await _agregar(Lectura, LecturaHora, desde, ahora)


async def job_agregar_dia():
    ahora = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    desde = ahora - timedelta(days=1)
    await _agregar(LecturaHora, LecturaDia, desde, ahora)


async def job_agregar_mes():
    ahora = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    desde = (ahora - timedelta(days=1)).replace(day=1)
    await _agregar(LecturaDia, LecturaMes, desde, ahora)


async def job_agregar_anio():
    ahora = datetime.utcnow().replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    desde = ahora.replace(year=ahora.year - 1)
    await _agregar(LecturaMes, LecturaAnio, desde, ahora)


async def job_limpiar_lecturas_crudas():
    limite = datetime.utcnow() - timedelta(days=7)
    async with AsyncSessionLocal() as db:
        await db.execute(delete(Lectura).where(Lectura.timestamp < limite))
        await db.commit()


def iniciar_scheduler() -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()
    scheduler.add_job(job_agregar_hora,          "cron", minute=0)
    scheduler.add_job(job_agregar_dia,           "cron", hour=0, minute=5)
    scheduler.add_job(job_agregar_mes,           "cron", day=1, hour=0, minute=10)
    scheduler.add_job(job_agregar_anio,          "cron", month=1, day=1, hour=0, minute=15)
    scheduler.add_job(job_limpiar_lecturas_crudas, "cron", hour=2, minute=0)
    scheduler.start()
    return scheduler
