"""Conexiones SQLite con transacciones y cierre garantizado."""

import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parents[2] / "practicas.sqlite3"


@contextmanager
def get_connection(database_path: str | Path = DATABASE_PATH) -> Iterator[sqlite3.Connection]:
    """Abre una conexión; confirma al terminar o revierte si ocurre un error."""
    connection = sqlite3.connect(database_path)
    try:
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        with connection:
            yield connection
    finally:
        connection.close()
