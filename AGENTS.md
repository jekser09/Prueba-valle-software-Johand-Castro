# Guía de trabajo para agentes

## Contexto y fuente de requisitos

Este repositorio corresponde a la prueba práctica de desarrollo asistido por IA de Johand Esteban Castro Rodríguez para el cargo de Director del Valle del Software de la Institución Universitaria de Colombia.

La fuente de requisitos es `Prueba_practica_Johand_Castro.pdf`. Consultarla ante dudas y actualizar la especificación cuando los evaluadores introduzcan cambios. La prueba es presencial y tiene una duración de 75 minutos; se valora el criterio, la calidad de las decisiones y el control sobre el código generado, aunque no se complete todo.

## Alcance funcional mínimo

Construir un sistema de seguimiento de prácticas profesionales que permita:

- Registrar estudiantes, empresas y asignaciones de práctica.
- Registrar las horas semanales reportadas por cada estudiante.
- Consultar el avance de horas de cada estudiante frente a las horas requeridas mediante una vista o un endpoint, para apoyar a coordinación.
- Aplicar validaciones básicas a los datos de entrada.

El PDF no fija campos, rutas, valores de horas requeridas ni reglas detalladas. Definirlos en la especificación, aclarar dudas con los evaluadores y dejar explícitos los supuestos. No presentar decisiones de implementación como requisitos originales.

## Flujo de trabajo solicitado

1. **Especificación — 10 minutos:** antes de implementar funcionalidades, redactar un documento breve con entidades y campos, endpoints o funcionalidades, reglas de negocio, criterios de aceptación y exclusiones de alcance.
2. **Construcción con IA — 35 minutos:** implementar el alcance mínimo conforme a la especificación.
3. **Ajuste de requisitos — 10 minutos:** incorporar el cambio indicado por los evaluadores tanto en la especificación como en el código. No anticipar un cambio concreto que aún no se haya solicitado.
4. **Revisión de código — 10 minutos:** documentar los problemas del fragmento de la Parte 4, su gravedad, las correcciones propuestas y las medidas que tomaría el líder del área para evitar su repetición.
5. **Presentación — 10 minutos:** explicar a los directivos qué se construyó, qué quedó pendiente y por qué, cómo distribuir el trabajo entre practicantes y cómo controlar los riesgos del desarrollo asistido por IA.

## Criterios para trabajar en el repositorio

- Explicar las acciones, las solicitudes a la IA y los motivos de las decisiones, conforme a la instrucción de pensar en voz alta durante la prueba.
- Trabajar con Git desde el inicio y realizar commits a medida que se avance.
- Se permite usar IA y documentación de internet. Revisar el código generado y verificar su comportamiento antes de darlo por terminado.
- El stack es libre: Python con FastAPI, SQLite y un frontend sencillo son sugerencias del PDF, no obligaciones. El repositorio parte de una estructura Python con `pyproject.toml`, paquete bajo `src/` y backend de construcción `uv_build`.
- Priorizar un flujo mínimo verificable y mantener documentadas las decisiones, los supuestos y los pendientes.
- Mantener la documentación en español y distinguir funcionalidades implementadas de objetivos pendientes.

## Revisión de código y calidad

El fragmento de la Parte 4 es material para analizar; no debe copiarse como base sin corregirlo. Como guía para la revisión y la implementación:

- Identificar el secreto incrustado y explicar su retirada y, si fuera real, su revocación o rotación. No reproducirlo en la documentación ni en el código.
- Evitar SQL construido con interpolación de entradas; usar consultas parametrizadas.
- Validar los datos y la existencia de las entidades relacionadas según las reglas acordadas.
- Cerrar conexiones y gestionar las transacciones de forma segura.
- Manejar los errores de forma explícita, sin ocultarlos ni responder con éxito cuando una operación falla.
- Evaluar la protección de los datos de estudiantes y los controles de acceso necesarios antes de producción; documentar lo que quede fuera del alcance de la prueba.
- Proponer medidas de liderazgo: revisión de cambios, formación, criterios de aceptación y verificaciones de calidad y seguridad sobre el código generado con IA.

Estas pautas orientan el análisis del fragmento; no sustituyen las notas de revisión exigidas como entregable.

## Entregables y cierre

- Repositorio Git o carpeta comprimida con el código y el historial de commits.
- Documento de especificación de la Parte 1, actualizado con el cambio de la Parte 3.
- Notas de revisión de código de la Parte 4.

Antes de cerrar una implementación, contrastar el resultado con los criterios de aceptación, registrar las verificaciones realizadas y señalar lo pendiente. Este `AGENTS.md` y el `README.md` orientan el proyecto, pero no sustituyen la especificación ni las notas de revisión.
