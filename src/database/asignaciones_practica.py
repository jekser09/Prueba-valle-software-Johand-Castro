"""Acceso a la tabla asignaciones_practica; todas las entradas usan parámetros SQL."""

from sqlite3 import Connection


def listar(connection: Connection) -> list[dict]:
    return [dict(row) for row in connection.execute("SELECT * FROM asignaciones_practica ORDER BY id")]


def obtener(connection: Connection, id: int) -> dict | None:
    row = connection.execute("SELECT * FROM asignaciones_practica WHERE id = ?", (id,)).fetchone()
    return dict(row) if row else None


def crear(connection: Connection, datos: dict) -> dict:
    cursor = connection.execute(
        "INSERT INTO asignaciones_practica (estudiante_id, empresa_id, fecha_inicio, horas_requeridas_centesimas) VALUES (?, ?, ?, ?)",
        (datos["estudiante_id"], datos["empresa_id"], datos["fecha_inicio"], datos["horas_requeridas_centesimas"],),
    )
    return obtener(connection, cursor.lastrowid)


def actualizar(connection: Connection, id: int, datos: dict) -> dict | None:
    connection.execute(
        "UPDATE asignaciones_practica SET estudiante_id = ?, empresa_id = ?, fecha_inicio = ?, horas_requeridas_centesimas = ? WHERE id = ?",
        (datos["estudiante_id"], datos["empresa_id"], datos["fecha_inicio"], datos["horas_requeridas_centesimas"], id),
    )
    return obtener(connection, id)


def eliminar(connection: Connection, id: int) -> None:
    connection.execute("DELETE FROM asignaciones_practica WHERE id = ?", (id,))

