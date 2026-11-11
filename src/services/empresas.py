"""Operaciones de empresas; la persistencia se delega a database."""

from src.database import empresas as repository
from src.schemas.empresa import EmpresaCreate
from src.services.common import operation, require


def listar() -> list[dict]:
    with operation() as connection:
        return repository.listar(connection)


def obtener(id: int) -> dict:
    with operation() as connection:
        return require(repository.obtener(connection, id), "Empresa")


def crear(datos: EmpresaCreate) -> dict:
    with operation(write=True) as connection:
        return repository.crear(connection, datos.model_dump())


def actualizar(id: int, datos: EmpresaCreate) -> dict:
    with operation(write=True) as connection:
        require(repository.obtener(connection, id), "Empresa")
        return repository.actualizar(connection, id, datos.model_dump())


def eliminar(id: int) -> None:
    with operation(write=True) as connection:
        require(repository.obtener(connection, id), "Empresa")
        repository.eliminar(connection, id)

