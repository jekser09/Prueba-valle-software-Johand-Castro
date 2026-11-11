"""Esquemas de empresas."""

from src.schemas.common import Correo, Identificador, SchemaBase, TextoObligatorio


class EmpresaCreate(SchemaBase):
    nit: TextoObligatorio
    nombre: TextoObligatorio
    correo_contacto: Correo


class EmpresaRead(EmpresaCreate):
    id: Identificador
