import uuid
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from typing import Optional
from database import Base

class Dispositivo(Base):
    __tablename__ = "dispositivos"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    ble_mac_address: Mapped[str] = mapped_column(String(17), unique=True, nullable=False)
    firmware_version: Mapped[Optional[str]] = mapped_column(String(20))
    ultimo_diagnostico: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="dispositivos")
    lecturas: Mapped[list["Lectura"]] = relationship(back_populates="dispositivo")
    diagnosticos: Mapped[list["Diagnostico"]] = relationship(back_populates="dispositivo")
    alertas: Mapped[list["Alerta"]] = relationship(back_populates="dispositivo")
