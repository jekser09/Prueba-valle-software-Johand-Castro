"""Acceso a la tabla empresas; todas las entradas usan parámetros SQL."""

from sqlite3 import Connection


def listar(connection: Connection) -> list[dict]:
    return [dict(row) for row in connection.execute("SELECT * FROM empresas ORDER BY id")]


def obtener(connection: Connection, id: int) -> dict | None:
    row = connection.execute("SELECT * FROM empresas WHERE id = ?", (id,)).fetchone()
    return dict(row) if row else None


def crear(connection: Connection, datos: dict) -> dict:
    cursor = connection.execute(
        "INSERT INTO empresas (nit, nombre, correo_contacto) VALUES (?, ?, ?)",
        (datos["nit"], datos["nombre"], datos["correo_contacto"],),
    )
    return obtener(connection, cursor.lastrowid)


def actualizar(connection: Connection, id: int, datos: dict) -> dict | None:
    connection.execute(
        "UPDATE empresas SET nit = ?, nombre = ?, correo_contacto = ? WHERE id = ?",
        (datos["nit"], datos["nombre"], datos["correo_contacto"], id),
    )
    return obtener(connection, id)


def eliminar(connection: Connection, id: int) -> None:
    connection.execute("DELETE FROM empresas WHERE id = ?", (id,))

