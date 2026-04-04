import uuid
from sqlalchemy import String, Float, Boolean, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from database import Base

class ComponenteDetectado(Base):
    __tablename__ = "componentes_detectados"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    diagnostico_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("diagnosticos.id"), nullable=False)
    tipo: Mapped[str] = mapped_column(String(50), nullable=False)
    etiqueta: Mapped[str] = mapped_column(String(100), nullable=False)
    confianza_yolo: Mapped[float] = mapped_column(Float, default=0.0)
    editado_por_usuario: Mapped[bool] = mapped_column(Boolean, default=False)
    bbox_json: Mapped[str] = mapped_column(Text, nullable=True)

    diagnostico: Mapped["Diagnostico"] = relationship(back_populates="componentes")
