import uuid
from sqlalchemy import String, Float, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from typing import Optional
from database import Base

class PerfilVoltaje(Base):
    __tablename__ = "perfiles_voltaje_custom"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    voltaje_nominal: Mapped[float] = mapped_column(Float, nullable=False)
    voltaje_min: Mapped[float] = mapped_column(Float, nullable=False)
    voltaje_max: Mapped[float] = mapped_column(Float, nullable=False)
    corriente_max: Mapped[float] = mapped_column(Float, nullable=False)
    temperatura_max: Mapped[float] = mapped_column(Float, nullable=False)
    notas: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="perfiles")
