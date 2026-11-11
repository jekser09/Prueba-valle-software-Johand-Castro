# Parte 4 · Revisión del código generado con IA

Revisión del fragmento incluido en [Prueba_practica_Johand_Castro.pdf](Prueba_practica_Johand_Castro.pdf), a partir de las observaciones de Johand Esteban Castro Rodríguez.

## Problemas, gravedad y correcciones

### 1. Credencial escrita directamente en el código

**Gravedad: crítica si la credencial es real y está activa.**

Nunca debemos dejar secretos, claves de API o credenciales directamente en el código. Cualquier persona con acceso al archivo o al repositorio podría verlos y utilizarlos.

**Corrección:** retirar la credencial del código y cargarla desde una variable de entorno o un gestor de secretos cuando sea necesaria. Si ya fue expuesta, revocarla o rotarla; eliminarla del archivo no invalida las copias ni el historial de Git. Si no se utiliza, eliminar esa configuración.

### 2. Consultas construidas mediante interpolación

**Gravedad: alta para la consulta de búsqueda por nombre.**

Las dos consultas incorporan valores con interpolación de cadenas, un patrón inseguro que debemos reemplazar por consultas parametrizadas. En la búsqueda, `nombre` se incorpora directamente al SQL, lo que permite una inyección SQL y puede exponer información de otros estudiantes.

En el registro de horas, los parámetros están declarados como `int` y FastAPI valida su tipo. Esto limita la posibilidad de introducir SQL por esos parámetros en el fragmento mostrado; aun así, la consulta debe parametrizarse y no depender únicamente de esa validación.

**Corrección:** separar la instrucción SQL de sus valores y validar los datos de entrada. Por ejemplo:

```python
connection.execute(
    "SELECT * FROM estudiantes WHERE nombre = ?",
    (nombre,),
)
```

Aplicar el mismo mecanismo de parámetros a la inserción de horas, indicando explícitamente las columnas de la tabla.

### 3. Lógica y acceso a datos dentro de las rutas

**Gravedad: media; problema de mantenibilidad y separación de responsabilidades.**

La capa donde definimos las rutas debería encargarse de recibir las solicitudes y devolver las respuestas HTTP de la API. Mezclar allí las conexiones, las consultas y la lógica del programa dificulta revisar, probar y mantener el código.

**Corrección:** organizar el flujo como `routes → services → database`. Las rutas delegan las operaciones; los servicios aplican las reglas de negocio, y los archivos de persistencia de cada tabla contienen las consultas parametrizadas y el acceso a los datos.

## Medidas como líder del área

Para evitar que estos errores se repitan, capacitaría a los colaboradores en buenas prácticas: manejo de secretos, prevención de inyección SQL, validación de entradas y separación de responsabilidades.

La capacitación debe incluir la revisión del código generado con IA: cada colaborador debe comprender y poder explicar lo que incorpora. La acompañaría con revisión de cambios antes de integrarlos, verificaciones de secretos y pruebas de validaciones y acceso a datos.

Este documento desarrolla las tres observaciones indicadas por el candidato; no pretende ser una revisión exhaustiva del fragmento.
