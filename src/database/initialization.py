"""Creación inicial de las tablas sin eliminar información existente."""

from pathlib import Path

from src.database.connection import DATABASE_PATH, get_connection

SCHEMA_PATH = Path(__file__).with_name("schema.sql")


def initialize_database(database_path: str | Path = DATABASE_PATH) -> None:
    """Crea las tablas faltantes en una transacción; propaga los errores."""
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    with get_connection(database_path) as connection:
        connection.executescript("BEGIN;\n" + schema)
