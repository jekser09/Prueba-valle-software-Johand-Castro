"""Cálculo del avance con precisión decimal; las consultas viven en database."""

from decimal import Decimal, ROUND_HALF_UP

from src.database import estudiantes
from src.services.common import from_cents, operation, require


def calculate(record: dict) -> dict:
    result = {key: value for key, value in record.items() if not key.endswith("_centesimas")}
    reported = record["horas_reportadas_centesimas"]
    required = record["horas_requeridas_centesimas"]
    result["horas_reportadas"] = from_cents(reported)
    if required is None:
        return dict(result, horas_requeridas=None, horas_pendientes=None,
                    porcentaje_avance=None, estado="sin_asignacion")
    result.update(
        horas_requeridas=from_cents(required),
        horas_pendientes=from_cents(max(required - reported, 0)),
        porcentaje_avance=(Decimal(reported) / Decimal(required) * 100).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        ),
        estado="completada" if reported >= required else "en_curso",
    )
    return result


def listar() -> list[dict]:
    with operation() as connection:
        return [calculate(record) for record in estudiantes.consultar_avance(connection)]


def obtener(estudiante_id: int) -> dict:
    with operation() as connection:
        records = estudiantes.consultar_avance(connection, estudiante_id)
        return calculate(require(records[0] if records else None, "Estudiante"))
