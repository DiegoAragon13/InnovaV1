import uuid
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DispositivoCreate(BaseModel):
    nombre: str
    ble_mac_address: str

class DispositivoUpdate(BaseModel):
    nombre: str

class DispositivoOut(BaseModel):
    id: uuid.UUID
    nombre: str
    ble_mac_address: str
    firmware_version: Optional[str]
    ultimo_diagnostico: Optional[datetime]
    created_at: datetime

    model_config = {"from_attributes": True}