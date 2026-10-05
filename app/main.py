"""Módulo de identidad e imágenes de referencia para el reto de TC2007B.

El contrato de https://startdroid.com/api (Prácticas 6 y 8) más las imágenes de
la Práctica 10: `POST /api/imagenes`, `GET /api/imagenes/:clave` y el campo
`imagen` de los avisos. Las imágenes viven en un almacén de objetos (RustFS);
PostgreSQL solo guarda su clave.

    cp .env.example .env        # y cambia los secretos
    docker compose up -d
    → http://localhost:8000/api/health   ·   http://localhost:8000/docs
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select

from . import almacen, errors
from .config import settings
from .db import Base, SessionLocal, engine
from .models import Aviso
from .routers import auth, avisos, imagenes


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Crea las tablas si no existen. Para el reto alcanza; el día que cambies una
    # columna con datos reales, eso se llama migración y se hace con Alembic.
    Base.metadata.create_all(engine)
    almacen.preparar()
    with SessionLocal() as db:
        if db.scalar(select(Aviso).limit(1)) is None:
            db.add(Aviso(titulo="Bienvenidos al tablón", cuerpo="Este aviso lo publicó el servidor al crear la tabla. Los siguientes los publica un profesor desde la app.", autor="profesor"))
            db.commit()
    yield


app = FastAPI(title="Avisos · identidad e imágenes de referencia", lifespan=lifespan)
errors.instalar(app)

# Abierto a cualquier origen para desarrollo (la consola del curso, tu navegador).
# En producción, lista aquí solo los orígenes que de verdad te llaman.
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

app.include_router(auth.router, prefix="/api")
app.include_router(avisos.router, prefix="/api")
app.include_router(imagenes.router, prefix="/api")


@app.get("/api/health")
def health() -> dict:
    return {
        "ok": True,
        "api": "Avisos · identidad e imágenes de referencia (FastAPI + PostgreSQL + RustFS)",
        "identidad": "usuario y contraseña en /auth/login; después `Authorization: Bearer <accessToken>`",
        "accessTokenSegundos": settings.access_ttl_s,
        "refreshTokenSegundos": settings.refresh_ttl_s,
        "endpoints": [
            "POST   /api/auth/register   { usuario, password, codigoProfesor? }",
            "POST   /api/auth/login      { usuario, password }",
            "POST   /api/auth/refresh    { refreshToken }",
            "POST   /api/auth/logout     { refreshToken }",
            "DELETE /api/auth/sesiones   (Bearer) cierra todas tus sesiones",
            "GET    /api/auth/me         (Bearer)",
            "GET    /api/avisos?desde=:id (Bearer) solo los avisos con id mayor a :id",
            "GET    /api/avisos/stream   (Bearer) SSE: un evento `aviso` por cada aviso nuevo, hasta que el token expira",
            "POST   /api/avisos          (Bearer, rol profesor) { titulo, cuerpo, imagen? }",
            "DELETE /api/avisos/:id      (Bearer, rol profesor) y su imagen",
            "POST   /api/imagenes        (Bearer, rol profesor) multipart `archivo`: JPEG, PNG o WebP de hasta 2 MB",
            "GET    /api/imagenes/:clave (Bearer) la imagen; ETag y caché de un año",
        ],
    }
