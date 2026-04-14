from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid
from pydantic import BaseModel
from datetime import datetime

from database import get_db
from models.alerta import Alerta
from models.user import User
from models.dispositivo import Dispositivo
from routers.deps import current_user

router = APIRouter(prefix="/alertas", tags=["alertas"])

class AlertaOut(BaseModel):
    id: uuid.UUID
    dispositivo_id: uuid.UUID
    tipo: str
    mensaje: str
    severidad: str
    vista: bool
    created_at: datetime
    model_config = {"from_attributes": True}

@router.get("", response_model=list[AlertaOut])
async def listar(solo_no_vistas: bool = False, user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    # Obtener IDs de dispositivos del usuario
    disp_result = await db.execute(select(Dispositivo.id).where(Dispositivo.user_id == user.id))
    ids = [r[0] for r in disp_result.all()]
    query = select(Alerta).where(Alerta.dispositivo_id.in_(ids)).order_by(Alerta.created_at.desc()).limit(100)
    if solo_no_vistas:
        query = query.where(Alerta.vista == False)
    result = await db.execute(query)
    return result.scalars().all()

@router.put("/{id}/vista")
async def marcar_vista(id: uuid.UUID, user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Alerta).where(Alerta.id == id))
    alerta = result.scalar_one_or_none()
    if not alerta:
        raise HTTPException(status_code=404, detail="Alerta no encontrada")
    alerta.vista = True
    await db.commit()
    return {"detail": "ok"}
