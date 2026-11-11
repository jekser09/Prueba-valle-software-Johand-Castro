"""Endpoints provisionales: validan entradas pero aún no consultan ni guardan datos."""

from typing import Annotated

from fastapi import APIRouter, Path

from src.schemas.asignacion import AsignacionCreate
from src.schemas.common import EndpointResponse, HealthResponse
from src.schemas.empresa import EmpresaCreate
from src.schemas.estudiante import EstudianteCreate
from src.schemas.reporte_horas import ReporteHorasCreate

router = APIRouter()
IdRuta = Annotated[int, Path(gt=0)]


@router.get("/health", tags=["Estado"], response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@router.post("/estudiantes", tags=["Estudiantes"], response_model=EndpointResponse)
def registrar_estudiante(datos: EstudianteCreate) -> EndpointResponse:
    return EndpointResponse(endpoint="registrar_estudiante")


@router.get("/estudiantes", tags=["Estudiantes"], response_model=EndpointResponse)
def listar_estudiantes() -> EndpointResponse:
    return EndpointResponse(endpoint="listar_estudiantes")


@router.post("/empresas", tags=["Empresas"], response_model=EndpointResponse)
def registrar_empresa(datos: EmpresaCreate) -> EndpointResponse:
    return EndpointResponse(endpoint="registrar_empresa")


@router.get("/empresas", tags=["Empresas"], response_model=EndpointResponse)
def listar_empresas() -> EndpointResponse:
    return EndpointResponse(endpoint="listar_empresas")


@router.post("/asignaciones", tags=["Asignaciones"], response_model=EndpointResponse)
def registrar_asignacion(datos: AsignacionCreate) -> EndpointResponse:
    return EndpointResponse(endpoint="registrar_asignacion")


@router.get("/asignaciones", tags=["Asignaciones"], response_model=EndpointResponse)
def listar_asignaciones() -> EndpointResponse:
    return EndpointResponse(endpoint="listar_asignaciones")


@router.post("/reportes-horas", tags=["Reportes de horas"], response_model=EndpointResponse)
def registrar_reporte_horas(datos: ReporteHorasCreate) -> EndpointResponse:
    return EndpointResponse(endpoint="registrar_reporte_horas")


@router.get(
    "/asignaciones/{id}/reportes-horas",
    tags=["Reportes de horas"],
    response_model=EndpointResponse,
)
def listar_reportes_horas(id: IdRuta) -> EndpointResponse:
    return EndpointResponse(endpoint="listar_reportes_horas")


@router.get("/avance", tags=["Avance"], response_model=EndpointResponse)
def listar_avance() -> EndpointResponse:
    return EndpointResponse(endpoint="listar_avance")


@router.get("/estudiantes/{id}/avance", tags=["Avance"], response_model=EndpointResponse)
def consultar_avance_estudiante(id: IdRuta) -> EndpointResponse:
    return EndpointResponse(endpoint="consultar_avance_estudiante")
