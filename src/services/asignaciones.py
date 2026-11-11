"""Reglas de asignación y conversión de horas; sin SQL."""

from fastapi import HTTPException

from src.database import asignaciones_practica as repository
from src.database import empresas, estudiantes, reportes_horas
from src.schemas.asignacion import AsignacionCreate
from src.services.common import from_cents, operation, require, to_cents


def serialize(record: dict) -> dict:
    return {
        **{key: value for key, value in record.items() if key != "horas_requeridas_centesimas"},
        "horas_requeridas": from_cents(record["horas_requeridas_centesimas"]),
    }


def payload(datos: AsignacionCreate) -> dict:
    result = datos.model_dump(exclude={"horas_requeridas"})
    result["fecha_inicio"] = datos.fecha_inicio.isoformat()
    result["horas_requeridas_centesimas"] = to_cents(datos.horas_requeridas)
    return result


def validate_relations(connection, datos: AsignacionCreate) -> None:
    require(estudiantes.obtener(connection, datos.estudiante_id), "Estudiante")
    require(empresas.obtener(connection, datos.empresa_id), "Empresa")


def listar() -> list[dict]:
    with operation() as connection:
        return [serialize(record) for record in repository.listar(connection)]


def obtener(id: int) -> dict:
    with operation() as connection:
        return serialize(require(repository.obtener(connection, id), "Asignación"))


def crear(datos: AsignacionCreate) -> dict:
    with operation(write=True) as connection:
        validate_relations(connection, datos)
        return serialize(repository.crear(connection, payload(datos)))


def actualizar(id: int, datos: AsignacionCreate) -> dict:
    with operation(write=True) as connection:
        previous = require(repository.obtener(connection, id), "Asignación")
        validate_relations(connection, datos)
        reports = reportes_horas.listar_por_asignacion(connection, id)
        if reports and (
            previous["estudiante_id"] != datos.estudiante_id
            or previous["empresa_id"] != datos.empresa_id
        ):
            raise HTTPException(409, "No se puede cambiar el estudiante o empresa de una asignación con reportes.")
        if reportes_horas.hay_semanas_anteriores(connection, id, datos.fecha_inicio.isoformat()):
            raise HTTPException(409, "La nueva fecha de inicio dejaría reportes fuera de la práctica.")
        return serialize(repository.actualizar(connection, id, payload(datos)))


def eliminar(id: int) -> None:
    with operation(write=True) as connection:
        require(repository.obtener(connection, id), "Asignación")
        repository.eliminar(connection, id)
