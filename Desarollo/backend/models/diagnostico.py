import uuid
from sqlalchemy import String, Float, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from typing import Optional
from database import Base

class Diagnostico(Base):
    __tablename__ = "diagnosticos"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dispositivo_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("dispositivos.id"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    foto_url: Mapped[Optional[str]] = mapped_column(Text)
    estado_general: Mapped[str] = mapped_column(String(20), default="normal")
    perfil_voltaje: Mapped[str] = mapped_column(String(20), default="5V")
    voltaje: Mapped[Optional[float]] = mapped_column(Float)
    corriente: Mapped[Optional[float]] = mapped_column(Float)
    temperatura: Mapped[Optional[float]] = mapped_column(Float)
    vibracion: Mapped[Optional[float]] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    dispositivo: Mapped["Dispositivo"] = relationship(back_populates="diagnosticos")
    componentes: Mapped[list["ComponenteDetectado"]] = relationship(back_populates="diagnostico")
    alertas: Mapped[list["Alerta"]] = relationship(back_populates="diagnostico")
    recomendacion: Mapped[Optional["Recomendacion"]] = relationship(back_populates="diagnostico", uselist=False)
