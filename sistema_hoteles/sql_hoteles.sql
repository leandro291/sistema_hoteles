-- DROP DE TABLAS ANTERIORES PARA EVITAR CONFLICTOS
DROP TABLE IF EXISTS acompanante CASCADE;
DROP TABLE IF EXISTS pago CASCADE;
DROP TABLE IF EXISTS reserva_servicio CASCADE;
DROP TABLE IF EXISTS reserva_habitacion CASCADE;
DROP TABLE IF EXISTS reserva CASCADE;
DROP TABLE IF EXISTS habitacion CASCADE;
DROP TABLE IF EXISTS servicio CASCADE;
DROP TABLE IF EXISTS usuario CASCADE;
DROP TABLE IF EXISTS cliente CASCADE;
DROP TABLE IF EXISTS tipo_habitacion CASCADE;

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
    contrasena VARCHAR(255) NOT NULL, 
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
    id_tipo_habitacion INT REFERENCES tipo_habitacion(id_tipo_habitacion) ON DELETE CASCADE

);

CREATE TABLE reserva (

    id_reserva SERIAL PRIMARY KEY,
    fecha_reserva TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_entrada DATE NOT NULL,
    fecha_salida DATE NOT NULL,
    estado_reserva VARCHAR(50) NOT NULL,
    id_cliente INT REFERENCES cliente(id_cliente) ON DELETE CASCADE,
    id_usuario INT REFERENCES usuario(id_usuario) ON DELETE CASCADE
);



-- 3. TABLAS CON DEPENDENCIAS DE SEGUNDO NIVEL (Tablas intermedias y Pagos)

CREATE TABLE reserva_habitacion (

    id_reserva_habitacion SERIAL PRIMARY KEY,
    id_habitacion INT REFERENCES habitacion(id_habitacion) ON DELETE CASCADE,
    id_reserva INT REFERENCES reserva(id_reserva) ON DELETE CASCADE,
    precio_x_noche DECIMAL(10, 2) NOT NULL,
    es_titular BOOLEAN NOT NULL, 
    subtotal DECIMAL(10, 2) NOT NULL

);

CREATE TABLE reserva_servicio (

    id_reserva_servicio SERIAL PRIMARY KEY,
    id_servicio INT REFERENCES servicio(id_servicio) ON DELETE CASCADE,
    id_reserva INT REFERENCES reserva(id_reserva) ON DELETE CASCADE,
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
    id_reserva INT REFERENCES reserva(id_reserva) ON DELETE CASCADE,
    id_usuario INT REFERENCES usuario(id_usuario) ON DELETE CASCADE

);

-- 4. TABLAS CON DEPENDENCIAS DE TERCER NIVEL

CREATE TABLE acompanante (

    id_acompanante SERIAL PRIMARY KEY, 
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    tipo_documento VARCHAR(50),
    num_documento VARCHAR(50),
    telefono VARCHAR(20),
    id_reserva_habitacion INT REFERENCES reserva_habitacion(id_reserva_habitacion) ON DELETE CASCADE

);