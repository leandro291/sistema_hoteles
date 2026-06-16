-- 1. TABLAS MAESTRAS (Sin dependencias externas)

CREATE TABLE tipo_habitacion (
    id_tipo_habitacion SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    capacidad INT NOT NULL,
    descripcion TEXT
);

CREATE TABLE cliente (

    id_cliente SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    tipo_documento VARCHAR(50) NOT NULL,
    num_documento VARCHAR(50) NOT NULL,
    telefono VARCHAR(20),
    correo VARCHAR(150),
    direccion TEXT

);

CREATE TABLE usuario (

    id_usuario SERIAL PRIMARY KEY,
    nombre_usuario VARCHAR(100) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL, -- Evitamos usar la 'ñ'
    rol VARCHAR(50) NOT NULL
);

CREATE TABLE servicio (

    id_servicio SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10, 2) NOT NULL

);

-- 2. TABLAS CON DEPENDENCIAS DE PRIMER NIVEL

CREATE TABLE habitacion (

    id_habitacion SERIAL PRIMARY KEY,
    num_piso INT NOT NULL,
    num_habitacion VARCHAR(20) NOT NULL,
    estado VARCHAR(50) NOT NULL,
    id_tipo_habitacion INT REFERENCES tipo_habitacion(id_tipo_habitacion)

);

CREATE TABLE reserva (

    id_reserva SERIAL PRIMARY KEY,
    fecha_reserva TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_entrada DATE NOT NULL,
    fecha_salida DATE NOT NULL,
    estado_reserva VARCHAR(50) NOT NULL,
    id_cliente INT REFERENCES cliente(id_cliente),
    id_usuario INT REFERENCES usuario(id_usuario)
);





-- 3. TABLAS CON DEPENDENCIAS DE SEGUNDO NIVEL (Tablas intermedias y Pagos)

CREATE TABLE reserva_habitacion (

    id_reserva_habitacion SERIAL PRIMARY KEY,
    id_habitacion INT REFERENCES habitacion(id_habitacion),
    id_reserva INT REFERENCES reserva(id_reserva),
    precio_x_noche DECIMAL(10, 2) NOT NULL,
    es_titular BOOLEAN NOT NULL, -- Asumiendo que "Estitular" en el diagrama significa "Es titular"
    subtotal DECIMAL(10, 2) NOT NULL

);

CREATE TABLE reserva_servicio (

    id_reserva_servicio SERIAL PRIMARY KEY,
    id_servicio INT REFERENCES servicio(id_servicio),
    id_reserva INT REFERENCES reserva(id_reserva),
    precio_unitario DECIMAL(10, 2) NOT NULL,
    cantidad INT NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL

);

CREATE TABLE pago (

    id_pago SERIAL PRIMARY KEY,
    monto DECIMAL(10, 2) NOT NULL,
    fecha_pago TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metodo_pago VARCHAR(50) NOT NULL,
    tipo_comprobante VARCHAR(50) NOT NULL,
    estado_pago VARCHAR(50) NOT NULL,
    id_reserva INT REFERENCES reserva(id_reserva),
    id_usuario INT REFERENCES usuario(id_usuario)

);





-- 4. TABLAS CON DEPENDENCIAS DE TERCER NIVEL

CREATE TABLE acompanante (

    id_acompanante SERIAL PRIMARY KEY, -- Evitamos usar la 'ñ'
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    tipo_documento VARCHAR(50),
    num_documento VARCHAR(50),
    telefono VARCHAR(20),
    id_reserva_habitacion INT REFERENCES reserva_habitacion(id_reserva_habitacion)

);