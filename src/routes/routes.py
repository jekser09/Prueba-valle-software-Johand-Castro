"""Endpoints CRUD; las operaciones se delegan a la capa de servicios."""

from typing import Annotated

from fastapi import APIRouter, Path, Response

from src.schemas.asignacion import AsignacionCreate, AsignacionRead
from src.schemas.avance import AvanceRead
from src.schemas.common import HealthResponse
from src.schemas.empresa import EmpresaCreate, EmpresaRead
from src.schemas.estudiante import EstudianteCreate, EstudianteRead
from src.schemas.reporte_horas import ReporteHorasCreate, ReporteHorasRead
from src.services import asignaciones, avance, empresas, estudiantes, reportes_horas

router = APIRouter()
IdRuta = Annotated[int, Path(gt=0)]


@router.get("/health", tags=["Estado"], response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@router.post("/estudiantes", tags=["Estudiantes"], response_model=EstudianteRead, status_code=201)
def crear_estudiantes(datos: EstudianteCreate):
    return estudiantes.crear(datos)


@router.get("/estudiantes", tags=["Estudiantes"], response_model=list[EstudianteRead])
def listar_estudiantes():
    return estudiantes.listar()


@router.get("/estudiantes/{id}", tags=["Estudiantes"], response_model=EstudianteRead)
def obtener_estudiantes(id: IdRuta):
    return estudiantes.obtener(id)


@router.put("/estudiantes/{id}", tags=["Estudiantes"], response_model=EstudianteRead)
def actualizar_estudiantes(id: IdRuta, datos: EstudianteCreate):
    return estudiantes.actualizar(id, datos)


@router.delete("/estudiantes/{id}", tags=["Estudiantes"], status_code=204, response_class=Response)
def eliminar_estudiantes(id: IdRuta):
    estudiantes.eliminar(id)
    return Response(status_code=204)


@router.post("/empresas", tags=["Empresas"], response_model=EmpresaRead, status_code=201)
def crear_empresas(datos: EmpresaCreate):
    return empresas.crear(datos)


@router.get("/empresas", tags=["Empresas"], response_model=list[EmpresaRead])
def listar_empresas():
    return empresas.listar()


@router.get("/empresas/{id}", tags=["Empresas"], response_model=EmpresaRead)
def obtener_empresas(id: IdRuta):
    return empresas.obtener(id)


@router.put("/empresas/{id}", tags=["Empresas"], response_model=EmpresaRead)
def actualizar_empresas(id: IdRuta, datos: EmpresaCreate):
    return empresas.actualizar(id, datos)


@router.delete("/empresas/{id}", tags=["Empresas"], status_code=204, response_class=Response)
def eliminar_empresas(id: IdRuta):
    empresas.eliminar(id)
    return Response(status_code=204)


@router.post("/asignaciones", tags=["Asignaciones"], response_model=AsignacionRead, status_code=201)
def crear_asignaciones(datos: AsignacionCreate):
    return asignaciones.crear(datos)


@router.get("/asignaciones", tags=["Asignaciones"], response_model=list[AsignacionRead])
def listar_asignaciones():
    return asignaciones.listar()


@router.get("/asignaciones/{id}", tags=["Asignaciones"], response_model=AsignacionRead)
def obtener_asignaciones(id: IdRuta):
    return asignaciones.obtener(id)


@router.put("/asignaciones/{id}", tags=["Asignaciones"], response_model=AsignacionRead)
def actualizar_asignaciones(id: IdRuta, datos: AsignacionCreate):
    return asignaciones.actualizar(id, datos)


@router.delete("/asignaciones/{id}", tags=["Asignaciones"], status_code=204, response_class=Response)
def eliminar_asignaciones(id: IdRuta):
    asignaciones.eliminar(id)
    return Response(status_code=204)


@router.post("/reportes-horas", tags=["Reportes de horas"], response_model=ReporteHorasRead, status_code=201)
def crear_reportes_horas(datos: ReporteHorasCreate):
    return reportes_horas.crear(datos)


@router.get("/reportes-horas", tags=["Reportes de horas"], response_model=list[ReporteHorasRead])
def listar_reportes_horas():
    return reportes_horas.listar()


@router.get("/reportes-horas/{id}", tags=["Reportes de horas"], response_model=ReporteHorasRead)
def obtener_reportes_horas(id: IdRuta):
    return reportes_horas.obtener(id)


@router.put("/reportes-horas/{id}", tags=["Reportes de horas"], response_model=ReporteHorasRead)
def actualizar_reportes_horas(id: IdRuta, datos: ReporteHorasCreate):
    return reportes_horas.actualizar(id, datos)


@router.delete("/reportes-horas/{id}", tags=["Reportes de horas"], status_code=204, response_class=Response)
def eliminar_reportes_horas(id: IdRuta):
    reportes_horas.eliminar(id)
    return Response(status_code=204)


@router.get("/asignaciones/{id}/reportes-horas", tags=["Reportes de horas"], response_model=list[ReporteHorasRead])
def listar_reportes_asignacion(id: IdRuta):
    return reportes_horas.listar_por_asignacion(id)


@router.get("/avance", tags=["Avance"], response_model=list[AvanceRead])
def listar_avance():
    return avance.listar()


@router.get("/estudiantes/{id}/avance", tags=["Avance"], response_model=AvanceRead)
def consultar_avance_estudiante(id: IdRuta):
    return avance.obtener(id)
