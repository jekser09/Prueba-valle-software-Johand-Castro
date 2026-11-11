"""Registro y corrección de horas semanales; sin consultas SQL."""

from datetime import date, timedelta

from fastapi import HTTPException

from src.database import asignaciones_practica, reportes_horas as repository
from src.schemas.reporte_horas import ReporteHorasCreate
from src.services.common import from_cents, operation, require, to_cents


def serialize(record: dict) -> dict:
    return {
        **{key: value for key, value in record.items() if key != "horas_centesimas"},
        "horas": from_cents(record["horas_centesimas"]),
    }


def payload(datos: ReporteHorasCreate) -> dict:
    result = datos.model_dump(exclude={"horas"})
    result["semana_inicio"] = datos.semana_inicio.isoformat()
    result["horas_centesimas"] = to_cents(datos.horas)
    return result


def validate_assignment(connection, datos: ReporteHorasCreate) -> None:
    assignment = require(asignaciones_practica.obtener(connection, datos.asignacion_id), "Asignación")
    if datos.semana_inicio + timedelta(days=6) < date.fromisoformat(assignment["fecha_inicio"]):
        raise HTTPException(422, "La semana reportada termina antes del inicio de la práctica.")


def listar() -> list[dict]:
    with operation() as connection:
        return [serialize(record) for record in repository.listar(connection)]


def listar_por_asignacion(id: int) -> list[dict]:
    with operation() as connection:
        require(asignaciones_practica.obtener(connection, id), "Asignación")
        return [serialize(record) for record in repository.listar_por_asignacion(connection, id)]


def obtener(id: int) -> dict:
    with operation() as connection:
        return serialize(require(repository.obtener(connection, id), "Reporte"))


def crear(datos: ReporteHorasCreate) -> dict:
    with operation(write=True) as connection:
        validate_assignment(connection, datos)
        return serialize(repository.crear(connection, payload(datos)))


def actualizar(id: int, datos: ReporteHorasCreate) -> dict:
    with operation(write=True) as connection:
        require(repository.obtener(connection, id), "Reporte")
        validate_assignment(connection, datos)
        return serialize(repository.actualizar(connection, id, payload(datos)))


def eliminar(id: int) -> None:
    with operation(write=True) as connection:
        require(repository.obtener(connection, id), "Reporte")
        repository.eliminar(connection, id)
