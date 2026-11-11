"""Verifica el arranque repetido y las garantías de persistencia de SQLite."""

import sqlite3
import unittest
from pathlib import Path
from uuid import uuid4

from src.database.connection import get_connection
from src.database.initialization import initialize_database


class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.path = Path(__file__).parent / f"test-{uuid4().hex}.sqlite3"
        self.addCleanup(self.path.unlink, missing_ok=True)
        initialize_database(self.path)

    def seed_assignment(self):
        with get_connection(self.path) as connection:
            connection.execute(
                "INSERT INTO estudiantes VALUES (?, ?, ?, ?, ?)",
                (1, "001", "Ana", "ana@example.com", "Software"),
            )
            connection.execute(
                "INSERT INTO empresas VALUES (?, ?, ?, ?)",
                (1, "9001", "Empresa", "contacto@example.com"),
            )
            connection.execute(
                "INSERT INTO asignaciones_practica VALUES (?, ?, ?, ?, ?)",
                (1, 1, 1, "2026-11-02", 12000),
            )

    def test_reinitialization_preserves_data_and_recreates_missing_table(self):
        self.seed_assignment()
        with get_connection(self.path) as connection:
            connection.execute("DROP TABLE reportes_horas")
        initialize_database(self.path)
        with get_connection(self.path) as connection:
            tables = {
                row["name"] for row in connection.execute(
                    "SELECT name FROM sqlite_master WHERE type = 'table'"
                )
            }
            self.assertEqual(tables, {
                "estudiantes", "empresas", "asignaciones_practica", "reportes_horas"
            })
            self.assertEqual(connection.execute("SELECT documento FROM estudiantes").fetchone()[0], "001")

    def test_foreign_keys_are_enabled_for_each_connection(self):
        with self.assertRaises(sqlite3.IntegrityError):
            with get_connection(self.path) as connection:
                connection.execute(
                    "INSERT INTO asignaciones_practica VALUES (?, ?, ?, ?, ?)",
                    (1, 999, 999, "2026-11-02", 12000),
                )

    def test_weekly_duplicates_and_invalid_hours_are_rejected(self):
        self.seed_assignment()
        with get_connection(self.path) as connection:
            connection.execute(
                "INSERT INTO reportes_horas VALUES (?, ?, ?, ?, ?)",
                (1, 1, "2026-11-02", 125, None),
            )
        for hours in (0, -1, 16801, 125.5):
            with self.subTest(hours=hours), self.assertRaises(sqlite3.IntegrityError):
                with get_connection(self.path) as connection:
                    connection.execute(
                        "INSERT INTO reportes_horas VALUES (?, ?, ?, ?, ?)",
                        (2, 1, "2026-11-09", hours, None),
                    )
        with self.assertRaises(sqlite3.IntegrityError):
            with get_connection(self.path) as connection:
                connection.execute(
                    "INSERT INTO reportes_horas VALUES (?, ?, ?, ?, ?)",
                    (2, 1, "2026-11-02", 100, None),
                )

    def test_failed_transaction_is_rolled_back_and_connection_closed(self):
        with self.assertRaises(RuntimeError):
            with get_connection(self.path) as connection:
                connection.execute(
                    "INSERT INTO empresas VALUES (?, ?, ?, ?)",
                    (1, "9001", "Empresa", "contacto@example.com"),
                )
                raise RuntimeError("Fallo durante la operación")
        with self.assertRaises(sqlite3.ProgrammingError):
            connection.execute("SELECT 1")
        with get_connection(self.path) as reopened:
            self.assertEqual(reopened.execute("SELECT count(*) FROM empresas").fetchone()[0], 0)
