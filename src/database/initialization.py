"""Creación del archivo SQLite y sus tablas sin eliminar información existente."""

from pathlib import Path

from src.database.connection import DATABASE_PATH, get_connection

SCHEMA_PATH = Path(__file__).with_name("schema.sql")


def initialize_database(database_path: str | Path = DATABASE_PATH) -> None:
    """Prepara el directorio, crea el archivo si falta e inicializa las tablas."""
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    Path(database_path).parent.mkdir(parents=True, exist_ok=True)
    # sqlite3.connect crea el archivo automáticamente si todavía no existe.
    with get_connection(database_path) as connection:
        connection.executescript("BEGIN;\n" + schema)
