"""Esquemas de asignaciones; las horas se reciben en unidades de hora."""

from datetime import date
from decimal import Decimal
from typing import Annotated

from pydantic import Field

from src.schemas.common import Identificador, SchemaBase

HorasPositivas = Annotated[Decimal, Field(gt=0, max_digits=12, decimal_places=2, allow_inf_nan=False)]


class AsignacionCreate(SchemaBase):
    estudiante_id: Identificador
    empresa_id: Identificador
    fecha_inicio: date
    horas_requeridas: HorasPositivas


class AsignacionRead(AsignacionCreate):
    id: Identificador
