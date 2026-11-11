"""Acceso a la tabla reportes_horas; todas las entradas usan parámetros SQL."""

from sqlite3 import Connection


def listar(connection: Connection) -> list[dict]:
    return [dict(row) for row in connection.execute("SELECT * FROM reportes_horas ORDER BY id")]


def obtener(connection: Connection, id: int) -> dict | None:
    row = connection.execute("SELECT * FROM reportes_horas WHERE id = ?", (id,)).fetchone()
    return dict(row) if row else None


def crear(connection: Connection, datos: dict) -> dict:
    cursor = connection.execute(
        "INSERT INTO reportes_horas (asignacion_id, semana_inicio, horas_centesimas, observaciones) VALUES (?, ?, ?, ?)",
        (datos["asignacion_id"], datos["semana_inicio"], datos["horas_centesimas"], datos["observaciones"],),
    )
    return obtener(connection, cursor.lastrowid)


def actualizar(connection: Connection, id: int, datos: dict) -> dict | None:
    connection.execute(
        "UPDATE reportes_horas SET asignacion_id = ?, semana_inicio = ?, horas_centesimas = ?, observaciones = ? WHERE id = ?",
        (datos["asignacion_id"], datos["semana_inicio"], datos["horas_centesimas"], datos["observaciones"], id),
    )
    return obtener(connection, id)


def eliminar(connection: Connection, id: int) -> None:
    connection.execute("DELETE FROM reportes_horas WHERE id = ?", (id,))


def listar_por_asignacion(connection: Connection, asignacion_id: int) -> list[dict]:
    return [dict(row) for row in connection.execute(
        "SELECT * FROM reportes_horas WHERE asignacion_id = ? ORDER BY semana_inicio, id",
        (asignacion_id,),
    )]


def hay_semanas_anteriores(connection: Connection, asignacion_id: int, fecha_inicio: str) -> bool:
    return connection.execute(
        "SELECT 1 FROM reportes_horas WHERE asignacion_id = ? "
        "AND date(semana_inicio, '+6 days') < ? LIMIT 1",
        (asignacion_id, fecha_inicio),
    ).fetchone() is not None

