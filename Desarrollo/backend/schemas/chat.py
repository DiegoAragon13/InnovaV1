from pydantic import BaseModel
import uuid
from datetime import datetime

class ChatMensajeIn(BaseModel):
    mensaje: str

class ChatMensajeOut(BaseModel):
    id: uuid.UUID
    rol: str
    contenido: str
    created_at: datetime

    model_config = {"from_attributes": True}
