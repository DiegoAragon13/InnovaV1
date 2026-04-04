from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
import uuid

from database import get_db
from models.chat import ChatMensaje
from models.lectura import Lectura
from models.alerta import Alerta
from models.user import User
from schemas.chat import ChatMensajeIn, ChatMensajeOut
from routers.deps import current_user
from services.llm_service import chat_stream

router = APIRouter(prefix="/chat", tags=["chat"])

HISTORIAL_LIMIT = 10

@router.post("/{dispositivo_id}")
async def chat(dispositivo_id: uuid.UUID, data: ChatMensajeIn, user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    # Historial reciente
    hist_result = await db.execute(
        select(ChatMensaje)
        .where(ChatMensaje.dispositivo_id == dispositivo_id, ChatMensaje.user_id == user.id)
        .order_by(ChatMensaje.created_at.desc()).limit(HISTORIAL_LIMIT)
    )
    mensajes = hist_result.scalars().all()[::-1]
    historial = [{"role": m.rol, "content": m.contenido} for m in mensajes]

    # Contexto: última lectura
    lect_result = await db.execute(
        select(Lectura).where(Lectura.dispositivo_id == dispositivo_id)
        .order_by(Lectura.timestamp.desc()).limit(1)
    )
    ultima = lect_result.scalar_one_or_none()
    contexto = {
        "voltaje": ultima.voltaje if ultima else None,
        "corriente": ultima.corriente if ultima else None,
        "temperatura": ultima.temperatura if ultima else None,
        "alertas": [],
        "componentes": []
    }

    # Guardar mensaje del usuario
    db.add(ChatMensaje(user_id=user.id, dispositivo_id=dispositivo_id, rol="user", contenido=data.mensaje))
    await db.commit()

    respuesta_completa = []

    async def stream_and_save():
        async for chunk in chat_stream(historial, data.mensaje, contexto):
            respuesta_completa.append(chunk)
            yield chunk
        # Guardar respuesta del asistente
        async with db.begin():
            db.add(ChatMensaje(
                user_id=user.id,
                dispositivo_id=dispositivo_id,
                rol="assistant",
                contenido="".join(respuesta_completa)
            ))

    return StreamingResponse(stream_and_save(), media_type="text/plain")

@router.get("/{dispositivo_id}/historial", response_model=list[ChatMensajeOut])
async def historial(dispositivo_id: uuid.UUID, user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ChatMensaje)
        .where(ChatMensaje.dispositivo_id == dispositivo_id, ChatMensaje.user_id == user.id)
        .order_by(ChatMensaje.created_at.asc())
    )
    return result.scalars().all()

@router.delete("/{dispositivo_id}/historial", status_code=204)
async def limpiar(dispositivo_id: uuid.UUID, user: User = Depends(current_user), db: AsyncSession = Depends(get_db)):
    await db.execute(delete(ChatMensaje).where(ChatMensaje.dispositivo_id == dispositivo_id, ChatMensaje.user_id == user.id))
    await db.commit()
