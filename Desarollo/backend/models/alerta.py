import uuid
from sqlalchemy import String, Boolean, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from typing import Optional
from database import Base

class Alerta(Base):
    __tablename__ = "alertas"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    diagnostico_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("diagnosticos.id"), nullable=True)
    dispositivo_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("dispositivos.id"), nullable=False)
    tipo: Mapped[str] = mapped_column(String(30), nullable=False)
    mensaje: Mapped[str] = mapped_column(Text, nullable=False)
    severidad: Mapped[str] = mapped_column(String(20), default="advertencia")
    vista: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    diagnostico: Mapped[Optional["Diagnostico"]] = relationship(back_populates="alertas")
    dispositivo: Mapped["Dispositivo"] = relationship(back_populates="alertas")
