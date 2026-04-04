from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from database import engine, Base
import models  # importa todos los modelos para que Base los registre

from routers import auth, dispositivos, lecturas, diagnosticos, alertas, chat

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="ElectroScan API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(dispositivos.router)
app.include_router(lecturas.router)
app.include_router(diagnosticos.router)
app.include_router(alertas.router)
app.include_router(chat.router)

@app.get("/")
async def root():
    return {"status": "ok", "version": "0.1.0"}
