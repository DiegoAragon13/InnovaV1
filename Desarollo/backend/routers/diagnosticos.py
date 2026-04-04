import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid
from datetime import datetime

from database import get_db
from models.diagnostico import Diagnostico
from models.componente import ComponenteDetectado
from models.alerta import Alerta
from models.recomendacion import Recomendacion
from models.dispositivo import Dispositivo
from models.user import User
from schemas.diagnostico import DiagnosticoCreate, DiagnosticoOut
from routers.deps import current_user
from services.llm_service import generar_recomendaciones

router = APIRouter(prefix="/diagnosticos", tags=["diagnosticos"])

@router.post("", response_model=DiagnosticoOut, status_code=201)
async def crear(data: DiagnosticoCreate, user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    # Verificar que el dispositivo pertenece al usuario
    result = await db.execute(select(Dispositivo).where(Dispositivo.id == data.dispositivo_id, Dispositivo.user_id == user.id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")

    diagnostico = Diagnostico(
        dispositivo_id=data.dispositivo_id,
        user_id=user.id,
        foto_url=data.foto_url,
        perfil_voltaje=data.perfil_voltaje,
        voltaje=data.voltaje,
        corriente=data.corriente,
        temperatura=data.temperatura,
        vibracion=data.vibracion,
    )
    db.add(diagnostico)
    await db.flush()

    # Guardar componentes
    for c in data.componentes:
        db.add(ComponenteDetectado(diagnostico_id=diagnostico.id, **c.model_dump()))

    # Construir contexto para LLM
    contexto = {
        "componentes": [c.etiqueta for c in data.componentes],
        "voltaje": data.voltaje,
        "corriente": data.corriente,
        "temperatura": data.temperatura,
        "perfil_voltaje": data.perfil_voltaje,
        "alertas": []
    }

    # Generar recomendaciones con LLM
    resultado = await generar_recomendaciones(contexto)
    diagnostico.estado_general = resultado.get("estado_general", "normal")

    rec = Recomendacion(
        diagnostico_id=diagnostico.id,
        estado_general=diagnostico.estado_general,
        componentes_en_riesgo=json.dumps(resultado.get("componentes_en_riesgo", [])),
        recomendaciones_json=json.dumps(resultado.get("recomendaciones", [])),
    )
    db.add(rec)

    # Actualizar ultimo_diagnostico del dispositivo
    disp_result = await db.execute(select(Dispositivo).where(Dispositivo.id == data.dispositivo_id))
    disp = disp_result.scalar_one()
    disp.ultimo_diagnostico = datetime.utcnow()

    await db.commit()
    await db.refresh(diagnostico)
    return diagnostico

@router.get("", response_model=list[DiagnosticoOut])
async def historial(user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Diagnostico).where(Diagnostico.user_id == user.id)
        .order_by(Diagnostico.created_at.desc()).limit(50)
    )
    return result.scalars().all()

@router.get("/{id}", response_model=DiagnosticoOut)
async def detalle(id: uuid.UUID, user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Diagnostico).where(Diagnostico.id == id, Diagnostico.user_id == user.id))
    diagnostico = result.scalar_one_or_none()
    if not diagnostico:
        raise HTTPException(status_code=404, detail="Diagnóstico no encontrado")
    return diagnostico
