CREATE TABLE IF NOT EXISTS estudiantes (
    id INTEGER PRIMARY KEY,
    documento TEXT NOT NULL UNIQUE CHECK (length(trim(documento)) > 0),
    nombre TEXT NOT NULL CHECK (length(trim(nombre)) > 0),
    correo TEXT NOT NULL CHECK (length(trim(correo)) > 0),
    programa TEXT NOT NULL CHECK (length(trim(programa)) > 0)
);

CREATE TABLE IF NOT EXISTS empresas (
    id INTEGER PRIMARY KEY,
    nit TEXT NOT NULL UNIQUE CHECK (length(trim(nit)) > 0),
    nombre TEXT NOT NULL CHECK (length(trim(nombre)) > 0),
    correo_contacto TEXT NOT NULL CHECK (length(trim(correo_contacto)) > 0)
);

CREATE TABLE IF NOT EXISTS asignaciones_practica (
    id INTEGER PRIMARY KEY,
    estudiante_id INTEGER NOT NULL UNIQUE REFERENCES estudiantes(id),
    empresa_id INTEGER NOT NULL REFERENCES empresas(id),
    fecha_inicio TEXT NOT NULL,
    horas_requeridas_centesimas INTEGER NOT NULL
        CHECK (typeof(horas_requeridas_centesimas) = 'integer'
               AND horas_requeridas_centesimas > 0)
);

CREATE TABLE IF NOT EXISTS reportes_horas (
    id INTEGER PRIMARY KEY,
    asignacion_id INTEGER NOT NULL REFERENCES asignaciones_practica(id),
    semana_inicio TEXT NOT NULL,
    horas_centesimas INTEGER NOT NULL
        CHECK (typeof(horas_centesimas) = 'integer'
               AND horas_centesimas BETWEEN 1 AND 16800),
    observaciones TEXT,
    UNIQUE (asignacion_id, semana_inicio)
);
