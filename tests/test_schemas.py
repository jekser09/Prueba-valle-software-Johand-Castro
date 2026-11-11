"""Validaciones de entrada antes de implementar los servicios."""

import unittest
from datetime import date, timedelta
from decimal import Decimal

from pydantic import ValidationError

from src.schemas.asignacion import AsignacionCreate
from src.schemas.empresa import EmpresaCreate
from src.schemas.estudiante import EstudianteCreate
from src.schemas.reporte_horas import ReporteHorasCreate


class SchemaTests(unittest.TestCase):
    def test_student_strips_text_and_preserves_document_leading_zeros(self):
        student = EstudianteCreate(
            documento=" 001 ", nombre=" Ana ", correo=" ana@example.com ", programa=" Software "
        )
        self.assertEqual(student.documento, "001")
        self.assertEqual(student.nombre, "Ana")
        self.assertEqual(student.correo, "ana@example.com")

    def test_required_text_email_and_unknown_fields_are_validated(self):
        valid = dict(nit="001", nombre="Empresa", correo_contacto="contacto@example.com")
        for changes in (
            {"nombre": "   "}, {"correo_contacto": "sin-correo"},
            {"correo_contacto": "a@@example.com"}, {"campo_desconocido": 1},
        ):
            with self.subTest(changes=changes), self.assertRaises(ValidationError):
                EmpresaCreate(**(valid | changes))

    def test_assignment_rejects_invalid_ids_dates_and_hours(self):
        valid = dict(estudiante_id=1, empresa_id=1, fecha_inicio="2026-11-02", horas_requeridas="120.25")
        for changes in (
            {"estudiante_id": 0}, {"empresa_id": -1}, {"estudiante_id": True},
            {"fecha_inicio": "2026-02-30"}, {"horas_requeridas": "0"},
            {"horas_requeridas": "1.234"}, {"horas_requeridas": "NaN"},
        ):
            with self.subTest(changes=changes), self.assertRaises(ValidationError):
                AsignacionCreate(**(valid | changes))
        self.assertEqual(AsignacionCreate(**valid).horas_requeridas, Decimal("120.25"))

    def test_weekly_report_accepts_decimal_hours_and_rejects_invalid_values(self):
        monday = date.today() - timedelta(days=date.today().weekday())
        valid = dict(asignacion_id=1, semana_inicio=monday.isoformat(), horas="1.25")
        self.assertEqual(ReporteHorasCreate(**valid).horas, Decimal("1.25"))
        for changes in (
            {"horas": "0"}, {"horas": "-1"}, {"horas": "168.01"},
            {"horas": "1.234"}, {"semana_inicio": (monday + timedelta(days=1)).isoformat()},
            {"semana_inicio": (monday + timedelta(days=7)).isoformat()},
        ):
            with self.subTest(changes=changes), self.assertRaises(ValidationError):
                ReporteHorasCreate(**(valid | changes))
