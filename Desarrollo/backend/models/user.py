import uuid
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    unidad_temperatura: Mapped[str] = mapped_column(String(3), default="°C")
    perfil_voltaje_default: Mapped[str] = mapped_column(String(20), default="5V")
    notificaciones: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    dispositivos: Mapped[list["Dispositivo"]] = relationship(back_populates="user")
    sesiones: Mapped[list["Sesion"]] = relationship(back_populates="user")
    perfiles: Mapped[list["PerfilVoltaje"]] = relationship(back_populates="user")
