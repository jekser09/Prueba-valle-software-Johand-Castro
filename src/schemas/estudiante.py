"""Esquemas de estudiantes."""

from src.schemas.common import Correo, Identificador, SchemaBase, TextoObligatorio


class EstudianteCreate(SchemaBase):
    documento: TextoObligatorio
    nombre: TextoObligatorio
    correo: Correo
    programa: TextoObligatorio


class EstudianteRead(EstudianteCreate):
    id: Identificador
