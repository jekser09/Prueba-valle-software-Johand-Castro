"""Pruebas HTTP contra una base SQLite aislada, sin dependencias de cliente HTTP."""

import json
import unittest
from datetime import date, timedelta
from decimal import Decimal
from functools import partial
from pathlib import Path
from unittest.mock import patch
from uuid import uuid4

from main import app
from src.database.connection import get_connection
from src.database.initialization import initialize_database


class ApiTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.path = Path(__file__).parent / f"api-{uuid4().hex}.sqlite3"
        self.addCleanup(self.path.unlink, missing_ok=True)
        initialize_database(self.path)
        override = patch("src.services.common.get_connection", partial(get_connection, self.path))
        override.start()
        self.addCleanup(override.stop)
        self.monday = date.today() - timedelta(days=date.today().weekday())
        self.student = dict(documento="001", nombre="Ana", correo="ana@example.com", programa="Software")
        self.company = dict(nit="9001", nombre="Empresa", correo_contacto="contacto@example.com")

    async def request(self, method, path, body=None, expected=200):
        messages = []

        async def receive():
            return {"type": "http.request", "body": json.dumps(body).encode() if body is not None else b"", "more_body": False}

        async def send(message):
            messages.append(message)

        await app({
            "type": "http", "asgi": {"version": "3.0"}, "http_version": "1.1",
            "method": method, "scheme": "http", "path": path, "raw_path": path.encode(),
            "query_string": b"", "root_path": "", "headers": [(b"content-type", b"application/json")],
            "client": ("127.0.0.1", 1234), "server": ("test", 80),
        }, receive, send)
        status = next(message["status"] for message in messages if message["type"] == "http.response.start")
        raw_body = b"".join(message.get("body", b"") for message in messages if message["type"] == "http.response.body")
        data = json.loads(raw_body) if raw_body else None
        self.assertEqual(status, expected, (method, path, data))
        return data

    async def seed(self):
        await self.request("POST", "/estudiantes", self.student, 201)
        await self.request("POST", "/empresas", self.company, 201)
        assignment = dict(estudiante_id=1, empresa_id=1,
                          fecha_inicio=(self.monday - timedelta(days=7)).isoformat(), horas_requeridas="120")
        await self.request("POST", "/asignaciones", assignment, 201)
        return assignment

    async def test_crud_students_and_companies(self):
        for path, payload in (("/estudiantes", self.student), ("/empresas", self.company)):
            self.assertEqual(await self.request("GET", path), [])
            created = await self.request("POST", path, payload, 201)
            id = created["id"]
            self.assertEqual((await self.request("GET", f"{path}/{id}"))["nombre"], payload["nombre"])
            updated = await self.request("PUT", f"{path}/{id}", payload | {"nombre": "Nuevo nombre"})
            self.assertEqual(updated["nombre"], "Nuevo nombre")
            self.assertEqual(len(await self.request("GET", path)), 1)
            self.assertIsNone(await self.request("DELETE", f"{path}/{id}", expected=204))
            await self.request("GET", f"{path}/{id}", expected=404)

    async def test_crud_assignments_reports_and_advance(self):
        assignment = await self.seed()
        for week, hours in ((self.monday - timedelta(days=7), "30"), (self.monday, "25")):
            await self.request("POST", "/reportes-horas", dict(asignacion_id=1, semana_inicio=week.isoformat(), horas=hours), 201)
        self.assertEqual(len(await self.request("GET", "/reportes-horas")), 2)
        self.assertEqual(len(await self.request("GET", "/asignaciones/1/reportes-horas")), 2)
        self.assertEqual(len(await self.request("GET", "/asignaciones")), 1)
        self.assertEqual((await self.request("GET", "/asignaciones/1"))["estudiante_id"], 1)
        progress = await self.request("GET", "/estudiantes/1/avance")
        self.assertEqual(Decimal(progress["horas_reportadas"]), Decimal("55"))
        self.assertEqual(Decimal(progress["porcentaje_avance"]), Decimal("45.83"))
        self.assertEqual(Decimal(progress["horas_pendientes"]), Decimal("65"))
        report = await self.request("GET", "/reportes-horas/2")
        report.pop("id")
        await self.request("PUT", "/reportes-horas/2", report | {"horas": "95"})
        progress = await self.request("GET", "/estudiantes/1/avance")
        self.assertEqual(progress["estado"], "completada")
        self.assertEqual(Decimal(progress["porcentaje_avance"]), Decimal("104.17"))
        updated = await self.request("PUT", "/asignaciones/1", assignment | {"horas_requeridas": "150"})
        self.assertEqual(Decimal(updated["horas_requeridas"]), Decimal("150"))
        for id in (1, 2):
            await self.request("DELETE", f"/reportes-horas/{id}", expected=204)
        await self.request("DELETE", "/asignaciones/1", expected=204)
        self.assertEqual((await self.request("GET", "/avance"))[0]["estado"], "sin_asignacion")

    async def test_missing_entities_duplicates_and_protected_deletes(self):
        await self.seed()
        for path, payload in (("/estudiantes", self.student), ("/empresas", self.company)):
            await self.request("POST", path, payload, 409)
            await self.request("DELETE", f"{path}/1", expected=409)
        report = dict(asignacion_id=1, semana_inicio=self.monday.isoformat(), horas="1.25")
        await self.request("POST", "/reportes-horas", report, 201)
        await self.request("POST", "/reportes-horas", report, 409)
        await self.request("DELETE", "/asignaciones/1", expected=409)
        await self.request("POST", "/reportes-horas", report | {"asignacion_id": 999}, 404)
        for path in ("/estudiantes", "/empresas", "/asignaciones", "/reportes-horas"):
            await self.request("GET", f"{path}/999", expected=404)
            await self.request("DELETE", f"{path}/999", expected=404)
        await self.request("GET", "/estudiantes/999/avance", expected=404)
        await self.request("GET", "/asignaciones/999/reportes-horas", expected=404)

    async def test_invalid_week_and_assignment_changes_leave_data_unchanged(self):
        assignment = await self.seed()
        report = dict(asignacion_id=1, semana_inicio=self.monday.isoformat(), horas="1.25")
        await self.request("POST", "/reportes-horas", report, 201)
        await self.request("POST", "/reportes-horas", report | {
            "semana_inicio": (self.monday - timedelta(days=14)).isoformat()
        }, 422)
        await self.request("POST", "/empresas", self.company | {"nit": "9002"}, 201)
        await self.request("PUT", "/asignaciones/1", assignment | {"empresa_id": 2}, 409)
        await self.request("PUT", "/asignaciones/1", assignment | {
            "fecha_inicio": (self.monday + timedelta(days=7)).isoformat()
        }, 409)
        self.assertEqual((await self.request("GET", "/asignaciones/1"))["empresa_id"], 1)
        self.assertEqual(len(await self.request("GET", "/reportes-horas")), 1)

    async def test_decimal_precision_and_sql_injection_text(self):
        await self.seed()
        for offset, hours in ((7, "0.10"), (0, "0.20")):
            await self.request("POST", "/reportes-horas", dict(
                asignacion_id=1, semana_inicio=(self.monday - timedelta(days=offset)).isoformat(), horas=hours
            ), 201)
        progress = await self.request("GET", "/estudiantes/1/avance")
        self.assertEqual(Decimal(progress["horas_reportadas"]), Decimal("0.30"))
        name = "Robert'); DROP TABLE estudiantes; --"
        await self.request("PUT", "/estudiantes/1", self.student | {"nombre": name})
        self.assertEqual((await self.request("GET", "/estudiantes/1"))["nombre"], name)

    async def test_unassigned_student_and_validation(self):
        await self.request("POST", "/estudiantes", self.student, 201)
        progress = await self.request("GET", "/estudiantes/1/avance")
        self.assertIsNone(progress["horas_requeridas"])
        self.assertEqual(progress["estado"], "sin_asignacion")
        await self.request("POST", "/estudiantes", {}, 422)
        await self.request("GET", "/estudiantes/0", expected=422)
        await self.request("POST", "/asignaciones", dict(
            estudiante_id=1, empresa_id=999, fecha_inicio=self.monday.isoformat(), horas_requeridas="120"
        ), 404)

    async def test_update_conflicts_and_missing_records_preserve_existing_values(self):
        assignment = await self.seed()
        await self.request("POST", "/asignaciones", assignment, 409)
        await self.request("POST", "/estudiantes", self.student | {"documento": "002"}, 201)
        await self.request("PUT", "/estudiantes/2", self.student, 409)
        self.assertEqual((await self.request("GET", "/estudiantes/2"))["documento"], "002")
        report = dict(asignacion_id=1, semana_inicio=self.monday.isoformat(), horas="1.25")
        await self.request("POST", "/reportes-horas", report, 201)
        await self.request("POST", "/reportes-horas", report | {
            "semana_inicio": (self.monday - timedelta(days=7)).isoformat()
        }, 201)
        await self.request("PUT", "/reportes-horas/2", report | {"horas": "99"}, 409)
        self.assertEqual(Decimal((await self.request("GET", "/reportes-horas/2"))["horas"]), Decimal("1.25"))
        for path, payload in (("/estudiantes", self.student), ("/empresas", self.company),
                              ("/asignaciones", assignment), ("/reportes-horas", report)):
            await self.request("PUT", f"{path}/999", payload, 404)
