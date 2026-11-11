# Sistema de seguimiento de prácticas profesionales

Proyecto de la prueba práctica de desarrollo asistido por inteligencia artificial de **Johand Esteban Castro Rodríguez**, candidato al cargo de **Director del Valle del Software** de la **Institución Universitaria de Colombia**.

La aplicación tiene como propósito gestionar las prácticas profesionales de los estudiantes: registrar estudiantes y empresas, asignar las prácticas y recopilar los reportes semanales de horas. El área de coordinación podrá consultar el avance de cada estudiante frente a las horas requeridas.

Los requisitos y la dinámica de evaluación se encuentran en [Prueba_practica_Johand_Castro.pdf](Prueba_practica_Johand_Castro.pdf).

## Objetivo general

Desarrollar una aplicación que facilite el seguimiento de las prácticas profesionales, con información sobre las asignaciones y el cumplimiento de horas de cada estudiante, mediante un proceso de desarrollo asistido por IA con decisiones justificadas y código revisado.

## Objetivos específicos

- Registrar estudiantes y empresas participantes.
- Registrar las asignaciones de práctica de los estudiantes.
- Registrar las horas semanales reportadas por cada estudiante.
- Ofrecer una vista o un endpoint de avance de horas por estudiante frente a las horas requeridas.
- Incorporar validaciones básicas de los datos de entrada.
- Definir entidades, funcionalidades, reglas de negocio, criterios de aceptación y límites del alcance antes de implementar.
- Adaptar la especificación y el código al cambio de requisitos que indiquen los evaluadores.
- Analizar el código proporcionado en la prueba, clasificar sus problemas y proponer correcciones y medidas de prevención desde el liderazgo técnico.

## Desarrollo de la prueba

La prueba es presencial y dura **75 minutos**, distribuidos en cinco etapas:

| Etapa | Duración | Resultado esperado |
| --- | --- | --- |
| Especificación | 10 minutos | Documento breve con el alcance y los criterios de aceptación. |
| Construcción con IA | 35 minutos | Implementación del flujo funcional mínimo. |
| Ajuste de requisitos | 10 minutos | Especificación y código actualizados con el cambio solicitado. |
| Revisión de código | 10 minutos | Notas sobre problemas, gravedad, correcciones y prevención. |
| Presentación | 10 minutos | Exposición de resultados, pendientes, reparto del trabajo entre practicantes y riesgos del uso de IA. |

Se permite usar herramientas de IA y documentación de internet. Se solicita explicar las acciones y decisiones durante el desarrollo, usar Git desde el inicio y realizar commits conforme se avance. La evaluación valora el criterio, la calidad de las decisiones y el control sobre el código generado; no exige completar todo el alcance.

## Tecnología y estado actual

El proyecto utiliza Python y FastAPI, con `main.py` como punto de entrada en la raíz. La estructura inicial separa las responsabilidades:

```text
main.py                 # Aplicación FastAPI, ciclo de inicio y registro del router
src/
    __init__.py
    schemas/            # Esquemas Pydantic para entradas y salidas
        __init__.py
    database/           # Conexión, persistencia y consultas
        __init__.py
    services/           # Reglas y operaciones de negocio
        __init__.py
    routes/
        __init__.py
        routes.py       # Rutas de la API
```

`services` es el nombre elegido para la lógica del programa. Los esquemas validan la estructura de los datos, los servicios aplican las reglas de negocio y `database` gestiona su persistencia. El paquete `src/prueba_tecnica_johand_castro/` se conserva como parte de la plantilla original; el arranque de la API utiliza `main:app`.

La ruta `GET /health` devuelve `{"status": "ok"}` para comprobar la disponibilidad de la API. Las diez operaciones de negocio propuestas en `REQUIREMENTS.md` están registradas en `src/routes/routes.py`, con respuestas provisionales como `{"endpoint": "listar_estudiantes"}`. Todavía no consultan ni modifican la base de datos; los `POST` devuelven `200` provisionalmente, hasta implementar la creación real con `201`.

Los esquemas Pydantic están separados por entidad en `src/schemas/`, con modelos `Create` y `Read`, además de `AvanceRead`. Los `POST` validan el cuerpo de la petición: textos obligatorios, formato básico de correo, identificadores positivos, fechas, horas positivas con hasta dos decimales, límite semanal de 168 horas y semanas que comienzan en lunes y no son futuras. Los identificadores de las rutas también deben ser positivos. Las entradas inválidas devuelven `422`.

Los modelos de lectura quedan preparados para integrar los servicios; las respuestas actuales usan `EndpointResponse`. Las comprobaciones que requieren consultar datos, como existencia de entidades, duplicados y fecha de inicio de la práctica, quedan pendientes en la lógica de negocio.

## Ejecución local

Desde la raíz del repositorio, instalar las dependencias y arrancar el servidor con uv:

```powershell
uv sync
uv run uvicorn main:app --reload
```

La API estará disponible en `http://127.0.0.1:8000`, la comprobación en `/health` y la documentación interactiva en `/docs`.

FastAPI y Uvicorn están declarados en `pyproject.toml` y disponibles en el entorno local.

## Base de datos

Al iniciar la API, el ciclo de vida de FastAPI ejecuta `initialize_database()` y crea `practicas.sqlite3` en la raíz del proyecto. La ruta se resuelve desde el código y no depende del directorio de ejecución. Se utiliza `sqlite3`, incluido en Python.

El archivo `src/database/schema.sql` define las tablas `estudiantes`, `empresas`, `asignaciones_practica` y `reportes_horas`. `CREATE TABLE IF NOT EXISTS` permite reiniciar sin borrar datos y crear tablas faltantes; no modifica la estructura de tablas existentes ni sustituye un sistema de migraciones. Si la inicialización falla, el error impide el arranque de la API.

`get_connection()` activa las claves foráneas, permite consultar filas por nombre de columna, confirma las transacciones exitosas, revierte las fallidas y cierra la conexión al terminar:

```python
from src.database.connection import get_connection

with get_connection() as connection:
    estudiantes = connection.execute("SELECT * FROM estudiantes").fetchall()
```

Las horas se almacenan como centésimas enteras para conservar su precisión. Los archivos de base de datos locales se excluyen de Git. La propuesta de campos, rutas, reglas y criterios de aceptación se encuentra en [REQUIREMENTS.md](REQUIREMENTS.md). Los endpoints de negocio y el frontend siguen pendientes.

## Entregables

- Repositorio Git o carpeta comprimida con el código y el historial de commits.
- Documento de especificación, actualizado con el cambio de requisitos introducido durante la prueba.
- Notas de revisión del código incluido en el enunciado.

Las pautas para trabajar en el repositorio y los requisitos que deben preservarse están en [AGENTS.md](AGENTS.md). La especificación está en [REQUIREMENTS.md](REQUIREMENTS.md); las notas de revisión de código quedan pendientes.
