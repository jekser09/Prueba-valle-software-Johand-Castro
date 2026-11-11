"""Punto de entrada de la API de seguimiento de prácticas."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database.initialization import initialize_database
from src.routes.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Prepara la base de datos antes de aceptar peticiones."""
    initialize_database()
    yield

app = FastAPI(
    title="Sistema de seguimiento de prácticas",
    description="Gestión de estudiantes, empresas, prácticas y reportes de horas.",
    version="0.1.0",
    lifespan=lifespan,
)


app.include_router(router)
