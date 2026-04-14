import uuid
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LecturaCreate(BaseModel):
    dispositivo_id: uuid.UUID
    voltaje: Optional[float] = None
    corriente: Optional[float] = None
    temperatura: Optional[float] = None
    vibracion: Optional[float] = None

class LecturaOut(BaseModel):
    id: uuid.UUID
    voltaje: Optional[float]
    corriente: Optional[float]
    temperatura: Optional[float]
    vibracion: Optional[float]
    estado: str
    timestamp: datetime

    model_config = {"from_attributes": True}

class LecturaAgregadaOut(BaseModel):
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
    periodo_inicio: datetime

    model_config = {"from_attributes": True}
