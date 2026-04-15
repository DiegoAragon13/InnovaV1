from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os

from database import engine, Base
import models

from routers import auth, dispositivos, lecturas, diagnosticos, alertas, chat
from routers import estadisticas, perfiles, fotos
from jobs.agregacion import iniciar_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    scheduler = iniciar_scheduler()
    yield
    scheduler.shutdown()

app = FastAPI(title="ElectroScan API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir fotos locales
os.makedirs("./uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="./uploads"), name="uploads")

app.include_router(auth.router)
app.include_router(dispositivos.router)
app.include_router(lecturas.router)
app.include_router(diagnosticos.router)
app.include_router(alertas.router)
app.include_router(chat.router)
app.include_router(estadisticas.router)
app.include_router(perfiles.router)
app.include_router(fotos.router)

@app.get("/")
async def root():
    return {"status": "ok", "version": "0.1.0"}
