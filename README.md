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

El repositorio contiene una estructura inicial de proyecto Python, con configuración en `pyproject.toml`, código bajo `src/prueba_tecnica_johand_castro/` y `uv_build` como backend de construcción. El punto de entrada actual solo imprime un mensaje de bienvenida; las funcionalidades del sistema están pendientes de implementación.

El enunciado permite elegir el stack y sugiere **Python con FastAPI, SQLite y un frontend sencillo**. Estas tecnologías de aplicación todavía no están incorporadas como dependencias. La propuesta de campos, rutas, reglas y criterios de aceptación se encuentra en [REQUIREMENTS.md](REQUIREMENTS.md).

## Entregables

- Repositorio Git o carpeta comprimida con el código y el historial de commits.
- Documento de especificación, actualizado con el cambio de requisitos introducido durante la prueba.
- Notas de revisión del código incluido en el enunciado.

Las pautas para trabajar en el repositorio y los requisitos que deben preservarse están en [AGENTS.md](AGENTS.md). La especificación está en [REQUIREMENTS.md](REQUIREMENTS.md); las notas de revisión de código quedan pendientes.
