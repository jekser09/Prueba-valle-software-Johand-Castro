"""Esquemas y validaciones propias de un reporte semanal."""

from datetime import date
from decimal import Decimal
from typing import Annotated

from pydantic import Field, field_validator

from src.schemas.common import Identificador, SchemaBase


class ReporteHorasCreate(SchemaBase):
    asignacion_id: Identificador
    semana_inicio: date
    horas: Annotated[Decimal, Field(gt=0, le=168, decimal_places=2, allow_inf_nan=False)]
    observaciones: str | None = None

    @field_validator("semana_inicio")
    @classmethod
    def validar_semana(cls, value: date) -> date:
        if value.weekday() != 0:
            raise ValueError("La semana debe comenzar en lunes")
        if value > date.today():
            raise ValueError("No se pueden reportar semanas futuras")
        return value


class ReporteHorasRead(ReporteHorasCreate):
    id: Identificador
