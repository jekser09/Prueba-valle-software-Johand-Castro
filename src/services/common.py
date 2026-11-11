"""Transacciones, errores HTTP y conversiones compartidas; sin consultas SQL."""

import sqlite3
from contextlib import contextmanager
from decimal import Decimal

from fastapi import HTTPException

from src.database.connection import get_connection


@contextmanager
def operation(*, write: bool = False):
    try:
        with get_connection(write=write) as connection:
            yield connection
    except sqlite3.IntegrityError as error:
        raise HTTPException(
            status_code=409,
            detail="La operación genera un duplicado o afecta registros relacionados.",
        ) from error
    except sqlite3.OperationalError as error:
        raise HTTPException(status_code=503, detail="La base de datos no está disponible.") from error


def require(record: dict | None, entity: str) -> dict:
    if record is None:
        raise HTTPException(status_code=404, detail=f"{entity} no encontrado/a.")
    return record


def to_cents(hours: Decimal) -> int:
    return int(hours * 100)


def from_cents(cents: int) -> Decimal:
    return Decimal(cents) / 100
