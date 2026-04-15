import os
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from pydantic import BaseModel

from config import settings
from models.user import User
from routers.deps import current_user

router = APIRouter(prefix="/fotos", tags=["fotos"])

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_SIZE_MB = 10


class FotoOut(BaseModel):
    foto_url: str


@router.post("", response_model=FotoOut, status_code=201)
async def subir_foto(
    file: UploadFile = File(...),
    user: User = Depends(current_user)
):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Formato no permitido. Usa JPG, PNG o WebP.")

    contenido = await file.read()
    if len(contenido) > MAX_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail=f"La imagen no puede superar {MAX_SIZE_MB}MB.")

    if settings.FOTO_STORAGE == "local":
        os.makedirs(settings.FOTO_LOCAL_PATH, exist_ok=True)
        extension = file.filename.split(".")[-1] if file.filename else "jpg"
        nombre = f"{uuid.uuid4()}.{extension}"
        ruta = os.path.join(settings.FOTO_LOCAL_PATH, nombre)
        with open(ruta, "wb") as f:
            f.write(contenido)
        foto_url = f"/uploads/{nombre}"
    else:
        # S3 — implementar cuando se migre a producción
        raise HTTPException(status_code=501, detail="S3 no implementado aún.")

    return FotoOut(foto_url=foto_url)
