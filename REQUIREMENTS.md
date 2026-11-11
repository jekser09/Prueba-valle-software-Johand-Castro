# Especificación del sistema de seguimiento de prácticas

## Propósito y alcance

Gestionar estudiantes, empresas, asignaciones de práctica y reportes semanales de horas. Coordinación debe poder consultar el avance de cada estudiante frente a las horas requeridas. Por solicitud posterior, el alcance incluye CRUD completo de las cuatro entidades.

Fuente: [Prueba_practica_Johand_Castro.pdf](Prueba_practica_Johand_Castro.pdf). Este documento desarrolla la especificación de la Parte 1 y deberá actualizarse con el cambio que indiquen los evaluadores en la Parte 3. El CRUD, la persistencia y la consulta de avance están implementados en la API; la presentación y las notas de revisión de código quedan pendientes.

## Requisitos del enunciado

- Registrar estudiantes, empresas y asignaciones de práctica.
- Registrar las horas semanales reportadas por cada estudiante.
- Consultar el avance de horas por estudiante mediante una vista o un endpoint.
- Validar los datos de entrada.

Los campos, las rutas y las reglas que siguen son una propuesta de diseño para el alcance mínimo; el enunciado no los define. Los supuestos podrán ajustarse durante la prueba.

## Modelo de datos propuesto

Se proponen cuatro tablas: `estudiantes`, `empresas`, `asignaciones_practica` y `reportes_horas`.

La asignación almacena la relación entre estudiante y empresa y la meta de horas. Los reportes se guardan en una tabla independiente, con una fila por semana y asignación. Las horas acumuladas y el porcentaje se calculan al consultar; no se guardan como columnas ni necesitan otra tabla de totales. Así se conserva el historial y se evita mantener dos versiones del mismo total.

### Estudiantes

| Campo | Tipo lógico | Restricciones |
| --- | --- | --- |
| `id` | Entero | Clave primaria generada. |
| `documento` | Texto | Obligatorio, único; conservar como texto para admitir letras y ceros iniciales. |
| `nombre` | Texto | Obligatorio. |
| `correo` | Texto | Obligatorio, con formato de correo válido. |
| `programa` | Texto | Obligatorio; programa académico del estudiante. |

### Empresas

| Campo | Tipo lógico | Restricciones |
| --- | --- | --- |
| `id` | Entero | Clave primaria generada. |
| `nit` | Texto | Obligatorio, único; conservar como texto. |
| `nombre` | Texto | Obligatorio; nombre o razón social. |
| `correo_contacto` | Texto | Obligatorio, con formato de correo válido. |

### Asignaciones de práctica

| Campo | Tipo lógico | Restricciones |
| --- | --- | --- |
| `id` | Entero | Clave primaria generada. |
| `estudiante_id` | Entero | Clave foránea a `estudiantes.id`, obligatoria y única en este alcance mínimo. |
| `empresa_id` | Entero | Clave foránea a `empresas.id`, obligatoria. |
| `fecha_inicio` | Fecha | Obligatoria, formato `AAAA-MM-DD`. |
| `horas_requeridas` | Decimal | Obligatorio, mayor que cero, hasta dos decimales y 12 dígitos en total. |

Una empresa puede recibir varios estudiantes. Como simplificación inicial, cada estudiante tiene una sola asignación; el historial de varias prácticas o cambios de empresa queda fuera del alcance mínimo. La meta se establece por asignación, sin fijar una cantidad institucional que el enunciado no proporciona.

### Reportes de horas

| Campo | Tipo lógico | Restricciones |
| --- | --- | --- |
| `id` | Entero | Clave primaria generada. |
| `asignacion_id` | Entero | Clave foránea a `asignaciones_practica.id`, obligatoria. |
| `semana_inicio` | Fecha | Lunes de la semana reportada, formato `AAAA-MM-DD`. |
| `horas` | Decimal | Obligatorio, mayor que cero y hasta 168, con hasta dos decimales. |
| `observaciones` | Texto | Opcional. |

La combinación `asignacion_id` y `semana_inicio` es única. El estudiante se obtiene a través de la asignación, sin duplicar su identificador en el reporte. La semana comprende de lunes a domingo.

## Reglas de negocio y validaciones

1. Recortar espacios al inicio y al final de los textos. Rechazar campos obligatorios vacíos o compuestos solo por espacios.
2. Rechazar documentos de estudiante y NIT de empresa duplicados después de recortar espacios. Para este alcance, no validar dígitos de verificación ni formatos nacionales específicos.
3. Crear una asignación solo si el estudiante y la empresa existen; rechazar una segunda asignación para el mismo estudiante.
4. Registrar horas solo para una asignación existente. La semana reportada debe intersectar el período iniciado en `fecha_inicio`: su domingo no puede ser anterior a esa fecha. Se admite el lunes anterior a la fecha de inicio si pertenece a esa misma semana.
5. Rechazar semanas cuyo lunes sea posterior a la fecha actual del servidor. Se permite reportar la semana en curso; no se registra detalle diario en este alcance.
6. Aceptar horas fraccionarias con hasta dos decimales. El límite de 168 horas semanales es una validación de duración física, no una regla de jornada laboral de la institución.
7. Rechazar un segundo reporte para la misma asignación y semana, sin incrementar las horas ni reemplazar el reporte existente.
8. Los reportes se contabilizan directamente, sin flujo de aprobación. Permitir que el total supere la meta y mostrar el valor real.
9. Un estudiante sin asignación debe aparecer en la consulta de avance con estado `sin_asignacion`, cero horas reportadas y meta, horas pendientes y porcentaje en `null`.
10. Conservar la integridad referencial. Rechazar con `409` la eliminación de estudiantes o empresas con asignaciones y de asignaciones con reportes. No hacer eliminaciones en cascada.
11. Las actualizaciones mediante `PUT` reemplazan los campos editables y requieren el mismo cuerpo que el alta. Aplicar las mismas validaciones y unicidad al editar; no permitir cambiar el identificador generado.
12. Si una asignación tiene reportes, no permitir cambiar su estudiante ni su empresa (`409`). Rechazar también cambios de fecha de inicio que dejen semanas existentes fuera del período válido (`409`). Se permite actualizar su meta de horas y recalcular el avance.
13. Permitir corregir y eliminar reportes; el avance se recalcula desde los datos vigentes. Las correcciones deben respetar la asignación, la semana, las horas y la unicidad. No se incluye un historial de auditoría.

Estas reglas son supuestos de diseño y deberán revisarse si los evaluadores establecen condiciones diferentes.

## Cálculo del avance

### Representación física en SQLite

Las horas se expresan como decimales en el modelo lógico y la API. Para conservar la precisión de las sumas, SQLite almacena centésimas de hora como enteros: `asignaciones_practica.horas_requeridas_centesimas` y `reportes_horas.horas_centesimas`. Por ejemplo, 1,25 horas se guardan como 125. Los servicios convierten entre ambas representaciones usando `Decimal`; las respuestas JSON serializan los decimales como cadenas, por ejemplo `"1.25"`. Las fechas se almacenan como texto ISO `AAAA-MM-DD`; los esquemas validan fechas y el formato básico de los correos, y los servicios validan las reglas entre registros.

Las consultas SQL y la agregación de horas viven en los archivos de cada tabla dentro de `src/database/`. Los servicios no ejecutan SQL; coordinan las transacciones, validan las reglas y calculan el porcentaje de avance.

Para una asignación:

```text
horas_reportadas = suma de horas de sus reportes, o 0 si no hay reportes
horas_pendientes = máximo(horas_requeridas - horas_reportadas, 0)
porcentaje_avance = redondear(horas_reportadas / horas_requeridas * 100, 2)
estado = completada si horas_reportadas >= horas_requeridas; en_curso en otro caso
```

El porcentaje puede superar el 100 %. El estado se deriva de las horas y no se almacena. Las sumas deben conservar la precisión decimal; el redondeo del porcentaje se aplica al presentar el resultado.

Ejemplo: para una meta de 120 horas y reportes de 30 y 25, se muestran 55 horas reportadas, 65 pendientes y un avance de 45,83 %.

## Funcionalidades y endpoints propuestos

El alcance mínimo puede entregarse mediante una API; el frontend es opcional según el tiempo disponible.

| Método | Ruta | Funcionalidad |
| --- | --- | --- |
| `POST` | `/estudiantes` | Registrar un estudiante. |
| `GET` | `/estudiantes` | Listar estudiantes. |
| `POST` | `/empresas` | Registrar una empresa. |
| `GET` | `/empresas` | Listar empresas. |
| `POST` | `/asignaciones` | Asignar un estudiante a una empresa y establecer su meta de horas. |
| `GET` | `/asignaciones` | Listar las asignaciones. |
| `POST` | `/reportes-horas` | Registrar las horas de una semana para una asignación. |
| `GET` | `/reportes-horas` | Listar todos los reportes. |
| `GET` | `/asignaciones/{id}/reportes-horas` | Consultar los reportes de una asignación en orden de semana ascendente. |
| `GET` | `/avance` | Consultar todos los estudiantes, con su asignación, empresa, meta, horas reportadas, horas pendientes, porcentaje y estado. |
| `GET` | `/estudiantes/{id}/avance` | Consultar el avance de un estudiante. |

Para cada recurso `/estudiantes`, `/empresas`, `/asignaciones` y `/reportes-horas` se incluyen además:

| Método | Ruta | Funcionalidad |
| --- | --- | --- |
| `GET` | `/{recurso}/{id}` | Obtener un registro por su identificador. |
| `PUT` | `/{recurso}/{id}` | Reemplazar los campos editables y devolver el registro actualizado (`200`). |
| `DELETE` | `/{recurso}/{id}` | Eliminar un registro sin dependencias (`204`, sin cuerpo). |

Las altas reciben JSON con los campos de cada entidad, excepto el identificador generado. Deben devolver el registro creado y su identificador con estado `201`. Las consultas exitosas devuelven `200`; los listados vacíos devuelven `[]`.

Las respuestas de error deben ser claras y no exponer SQL ni detalles internos: `404` para entidades inexistentes, `409` para duplicados o conflictos con registros relacionados, `422` para datos inválidos y `503` si la base de datos no está disponible. Una operación fallida no debe responder como exitosa ni dejar registros parciales.

## Criterios de aceptación

| Caso | Resultado esperado |
| --- | --- |
| Registrar un estudiante y una empresa con datos válidos. | Ambos reciben un identificador y aparecen en sus listados. |
| Enviar un nombre vacío o un correo inválido. | Se rechaza la petición con `422` y no se crea el registro. |
| Repetir un documento de estudiante o un NIT. | Se responde `409` y se conserva un único registro. |
| Asignar un estudiante y una empresa existentes con meta de 120 horas. | Se crea una asignación que conserva ambas referencias y la meta. |
| Asignar un estudiante o una empresa inexistentes. | Se responde `404` sin crear la asignación. |
| Crear una segunda asignación para el mismo estudiante. | Se responde `409`. |
| Registrar 30 y 25 horas en dos semanas válidas distintas. | Ambos reportes se conservan; el avance muestra 55 horas, 65 pendientes y 45,83 %. |
| Registrar horas negativas, cero, más de 168 o con más de dos decimales. | Se responde `422` sin modificar el avance. |
| Registrar un reporte para una asignación inexistente. | Se responde `404`. |
| Repetir un reporte de la misma asignación y semana. | Se responde `409` y el total permanece igual. |
| Enviar una fecha de semana que no sea lunes, sea futura o termine antes del inicio de la práctica. | Se responde `422`. |
| Consultar una asignación sin reportes con meta de 120 horas. | Se muestran 0 horas reportadas, 120 pendientes, 0 % y estado `en_curso`. |
| Alcanzar 125 horas frente a una meta de 120. | Se muestran 125 horas, 0 pendientes, 104,17 % y estado `completada`. |
| Consultar un estudiante sin asignación. | Aparece con estado `sin_asignacion` y valores según la regla 9. |
| Consultar el avance de un estudiante inexistente. | Se responde `404`. |
| Reiniciar la aplicación después de registrar información. | Los datos persisten y los cálculos se mantienen. |
| Consultar, actualizar o eliminar un identificador inexistente. | Se responde `404`. |
| Actualizar un registro con datos válidos mediante `PUT`. | Se responde `200` con los nuevos valores y el mismo identificador. |
| Actualizar un documento, NIT o semana generando un duplicado. | Se responde `409` y se conservan los valores anteriores. |
| Eliminar un registro sin dependencias. | Se responde `204` y deja de aparecer en las consultas. |
| Eliminar un registro con dependencias. | Se responde `409` sin eliminar datos relacionados. |
| Corregir o eliminar horas reportadas. | El avance refleja los reportes vigentes. |
| Cambiar una asignación con reportes de forma que invalide su historial. | Se responde `409` y se conserva la asignación anterior. |

## Fuera del alcance inicial

- Autenticación, roles y acceso de estudiantes o empresas mediante cuentas propias.
- Aprobación de horas por tutores, adjuntos y evidencias.
- Historial de múltiples prácticas por estudiante y traslados de empresa.
- Historial de auditoría de ediciones y eliminaciones.
- Validación de jornadas legales, convenios o condiciones académicas específicas no suministradas.
- Notificaciones, exportaciones, integraciones y despliegue de producción.
- Frontend avanzado; una API consultable satisface el mínimo del enunciado.

## Cambios de requisitos

No se ha recibido aún el cambio de la Parte 3. Cuando se indique, registrar aquí su descripción, las reglas y criterios de aceptación afectados y los ajustes realizados en la implementación.

### Ampliación solicitada durante el desarrollo

Se solicitó CRUD completo y acceso a datos separado por tabla. Se incorporaron archivos de persistencia por entidad en `database`, servicios sin SQL, operaciones `GET` por identificador, `PUT` y `DELETE`, y las reglas y criterios de aceptación correspondientes. Esta ampliación no se presenta como el cambio pendiente de los evaluadores de la Parte 3.
