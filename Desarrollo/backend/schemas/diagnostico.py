import uuid
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class ComponenteIn(BaseModel):
    tipo: str
    etiqueta: str
    confianza_yolo: float = 0.0
    editado_por_usuario: bool = False
    bbox_json: Optional[str] = None

class DiagnosticoCreate(BaseModel):
    dispositivo_id: uuid.UUID
    foto_url: Optional[str] = None
    perfil_voltaje: str = "5V"
    voltaje: Optional[float] = None
    corriente: Optional[float] = None
    temperatura: Optional[float] = None
    vibracion: Optional[float] = None
    componentes: List[ComponenteIn]

class DiagnosticoOut(BaseModel):
    id: uuid.UUID
    dispositivo_id: uuid.UUID
    foto_url: Optional[str]
    estado_general: str
    perfil_voltaje: str
    voltaje: Optional[float]
    corriente: Optional[float]
    temperatura: Optional[float]
    vibracion: Optional[float]
    created_at: datetime
    recomendaciones: Optional[list] = None

    model_config = {"from_attributes": True}
