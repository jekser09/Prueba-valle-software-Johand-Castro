"""Operaciones de estudiantes; la persistencia se delega a database."""

from src.database import estudiantes as repository
from src.schemas.estudiante import EstudianteCreate
from src.services.common import operation, require


def listar() -> list[dict]:
    with operation() as connection:
        return repository.listar(connection)


def obtener(id: int) -> dict:
    with operation() as connection:
        return require(repository.obtener(connection, id), "Estudiante")


def crear(datos: EstudianteCreate) -> dict:
    with operation(write=True) as connection:
        return repository.crear(connection, datos.model_dump())


def actualizar(id: int, datos: EstudianteCreate) -> dict:
    with operation(write=True) as connection:
        require(repository.obtener(connection, id), "Estudiante")
        return repository.actualizar(connection, id, datos.model_dump())


def eliminar(id: int) -> None:
    with operation(write=True) as connection:
        require(repository.obtener(connection, id), "Estudiante")
        repository.eliminar(connection, id)

