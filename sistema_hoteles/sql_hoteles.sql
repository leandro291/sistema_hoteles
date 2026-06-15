-- 1. TABLAS MAESTRAS
CREATE TABLE tipo_habitacion (
    id_tipo_habitacion SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE, 
    precio DECIMAL(10, 2) NOT NULL,
    capacidad INT NOT NULL,
    descripcion TEXT
);

CREATE TABLE cliente (
    id_cliente SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    tipo_documento VARCHAR(50) NOT NULL,
    num_documento VARCHAR(50) NOT NULL UNIQUE, 
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
    nombre VARCHAR(100) NOT NULL UNIQUE, 
    descripcion TEXT,
    precio DECIMAL(10, 2) NOT NULL
);

-- 2. TABLAS CON DEPENDENCIAS DE PRIMER NIVEL
CREATE TABLE habitacion (
    id_habitacion SERIAL PRIMARY KEY,
    num_piso INT NOT NULL,
    num_habitacion VARCHAR(20) NOT NULL UNIQUE, 
    estado VARCHAR(50) NOT NULL,
    id_tipo_habitacion INT REFERENCES tipo_habitacion(id_tipo_habitacion)
);

-- 3. TABLAS INTERMEDIAS CON LLAVES COMPUESTAS
CREATE TABLE reserva_habitacion (
    id_reserva_habitacion SERIAL PRIMARY KEY,
    id_habitacion INT REFERENCES habitacion(id_habitacion),
    id_reserva INT REFERENCES reserva(id_reserva),
    precio_x_noche DECIMAL(10, 2) NOT NULL,
    es_titular BOOLEAN NOT NULL, 
    subtotal DECIMAL(10, 2) NOT NULL,
    CONSTRAINT uq_reserva_habitacion UNIQUE (id_reserva, id_habitacion) 
);

CREATE TABLE reserva_servicio (
    id_reserva_servicio SERIAL PRIMARY KEY,
    id_servicio INT REFERENCES servicio(id_servicio),
    id_reserva INT REFERENCES reserva(id_reserva),
    precio_unitario DECIMAL(10, 2) NOT NULL,
    cantidad INT NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    CONSTRAINT uq_reserva_servicio UNIQUE (id_reserva, id_servicio) 
);