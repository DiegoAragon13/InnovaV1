import uuid
from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from typing import Optional
from database import Base

class Lectura(Base):
    __tablename__ = "lecturas"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dispositivo_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("dispositivos.id"), nullable=False)
    voltaje: Mapped[Optional[float]] = mapped_column(Float)
    corriente: Mapped[Optional[float]] = mapped_column(Float)
    temperatura: Mapped[Optional[float]] = mapped_column(Float)
    vibracion: Mapped[Optional[float]] = mapped_column(Float)
    estado: Mapped[str] = mapped_column(String(20), default="normal")
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow, index=True)

    dispositivo: Mapped["Dispositivo"] = relationship(back_populates="lecturas")


class _LecturaAgregadaBase(Base):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dispositivo_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    voltaje_avg: Mapped[Optional[float]] = mapped_column(Float)
    voltaje_min: Mapped[Optional[float]] = mapped_column(Float)
    voltaje_max: Mapped[Optional[float]] = mapped_column(Float)
    corriente_avg: Mapped[Optional[float]] = mapped_column(Float)
    corriente_min: Mapped[Optional[float]] = mapped_column(Float)
    corriente_max: Mapped[Optional[float]] = mapped_column(Float)
    temperatura_avg: Mapped[Optional[float]] = mapped_column(Float)
    temperatura_min: Mapped[Optional[float]] = mapped_column(Float)
    temperatura_max: Mapped[Optional[float]] = mapped_column(Float)
    vibracion_avg: Mapped[Optional[float]] = mapped_column(Float)
    vibracion_max: Mapped[Optional[float]] = mapped_column(Float)
    periodo_inicio: Mapped[datetime] = mapped_column(nullable=False, index=True)


class LecturaHora(_LecturaAgregadaBase):
    __tablename__ = "lecturas_hora"

class LecturaDia(_LecturaAgregadaBase):
    __tablename__ = "lecturas_dia"

class LecturaMes(_LecturaAgregadaBase):
    __tablename__ = "lecturas_mes"

class LecturaAnio(_LecturaAgregadaBase):
    __tablename__ = "lecturas_anio"
