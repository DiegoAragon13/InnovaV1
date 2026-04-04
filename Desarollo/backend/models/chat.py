import uuid
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional
from database import Base

class ChatMensaje(Base):
    __tablename__ = "chat_mensajes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    dispositivo_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("dispositivos.id"), nullable=False)
    rol: Mapped[str] = mapped_column(String(10), nullable=False)  # "user" | "assistant"
    contenido: Mapped[str] = mapped_column(Text, nullable=False)
    contexto_usado: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
