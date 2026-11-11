"""Contrato previsto para las consultas de avance."""

from decimal import Decimal
from typing import Annotated, Literal

from pydantic import Field

from src.schemas.asignacion import HorasPositivas
from src.schemas.common import Identificador, SchemaBase, TextoObligatorio

ValorNoNegativo = Annotated[Decimal, Field(ge=0, decimal_places=2, allow_inf_nan=False)]


class AvanceRead(SchemaBase):
    estudiante_id: Identificador
    estudiante_nombre: TextoObligatorio
    asignacion_id: Identificador | None
    empresa_id: Identificador | None
    empresa_nombre: TextoObligatorio | None
    horas_requeridas: HorasPositivas | None
    horas_reportadas: ValorNoNegativo
    horas_pendientes: ValorNoNegativo | None
    porcentaje_avance: ValorNoNegativo | None
    estado: Literal["sin_asignacion", "en_curso", "completada"]
