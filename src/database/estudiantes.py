"""Acceso a la tabla estudiantes; todas las entradas usan parámetros SQL."""

from sqlite3 import Connection


def listar(connection: Connection) -> list[dict]:
    return [dict(row) for row in connection.execute("SELECT * FROM estudiantes ORDER BY id")]


def obtener(connection: Connection, id: int) -> dict | None:
    row = connection.execute("SELECT * FROM estudiantes WHERE id = ?", (id,)).fetchone()
    return dict(row) if row else None


def crear(connection: Connection, datos: dict) -> dict:
    cursor = connection.execute(
        "INSERT INTO estudiantes (documento, nombre, correo, programa) VALUES (?, ?, ?, ?)",
        (datos["documento"], datos["nombre"], datos["correo"], datos["programa"],),
    )
    return obtener(connection, cursor.lastrowid)


def actualizar(connection: Connection, id: int, datos: dict) -> dict | None:
    connection.execute(
        "UPDATE estudiantes SET documento = ?, nombre = ?, correo = ?, programa = ? WHERE id = ?",
        (datos["documento"], datos["nombre"], datos["correo"], datos["programa"], id),
    )
    return obtener(connection, id)


def eliminar(connection: Connection, id: int) -> None:
    connection.execute("DELETE FROM estudiantes WHERE id = ?", (id,))


def consultar_avance(connection: Connection, estudiante_id: int | None = None) -> list[dict]:
    query = """
        SELECT e.id AS estudiante_id, e.nombre AS estudiante_nombre,
               a.id AS asignacion_id, a.empresa_id, em.nombre AS empresa_nombre,
               a.horas_requeridas_centesimas,
               COALESCE(SUM(r.horas_centesimas), 0) AS horas_reportadas_centesimas
        FROM estudiantes e
        LEFT JOIN asignaciones_practica a ON a.estudiante_id = e.id
        LEFT JOIN empresas em ON em.id = a.empresa_id
        LEFT JOIN reportes_horas r ON r.asignacion_id = a.id
    """
    parameters = ()
    if estudiante_id is not None:
        query += " WHERE e.id = ?"
        parameters = (estudiante_id,)
    query += " GROUP BY e.id, e.nombre, a.id, a.empresa_id, em.nombre, a.horas_requeridas_centesimas ORDER BY e.id"
    return [dict(row) for row in connection.execute(query, parameters)]

