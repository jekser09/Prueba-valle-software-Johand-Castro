"""Tipos compartidos para entradas y respuestas de la API."""

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

TextoObligatorio = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
Correo = Annotated[
    str,
    StringConstraints(strip_whitespace=True, pattern=r"^[^\s@]+@[^\s@]+\.[^\s@]+$"),
]
Identificador = Annotated[int, Field(strict=True, gt=0)]


class SchemaBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")


class EndpointResponse(SchemaBase):
    """Respuesta provisional mientras se implementan los servicios."""

    endpoint: str


class HealthResponse(SchemaBase):
    status: str
