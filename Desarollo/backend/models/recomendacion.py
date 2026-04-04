import uuid
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from typing import Optional
from database import Base

class Recomendacion(Base):
    __tablename__ = "recomendaciones"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    diagnostico_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("diagnosticos.id"), unique=True, nullable=False)
    estado_general: Mapped[str] = mapped_column(String(20), default="normal")
    componentes_en_riesgo: Mapped[Optional[str]] = mapped_column(Text)  # JSON array
    recomendaciones_json: Mapped[Optional[str]] = mapped_column(Text)   # JSON array
    prompt_usado: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    diagnostico: Mapped["Diagnostico"] = relationship(back_populates="recomendacion")
