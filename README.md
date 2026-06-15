# Hotel System Management - Beta V.1.00

Un sistema de gestión hotelera de escritorio robusto, modular y transaccional diseñado para optimizar las operaciones de recepción, facturación y auditoría. Desarrollado con un enfoque estricto en **Integridad de Datos** y **Arquitectura de Software Profesional**.

---

## Características Principales

* **Dashboard Interactivo:** Reportes en tiempo real de habitaciones disponibles, ocupadas y total de clientes registrados.
* **Gestión de Habitaciones:** CRUD completo con borrado lógico (inactivación) para proteger la integridad del historial. Gestión independiente de "Tipos de Habitación".
* **Control de Clientes:** Registro con validaciones estrictas (longitud de documentos, formatos de correo, bloqueo de caracteres numéricos en nombres).
* **Módulo de Caja y Liquidación:** Cálculos matemáticos precisos (uso de `Decimal`) para cobro de noches y servicios extra. Generación de tickets y liberación automática de habitaciones post-pago.
* **Transacciones Seguras (ACID):** Operaciones en cadena (Ej. Pago -> Finalizar Reserva -> Liberar Habitación) blindadas con `commit` y `rollback` para evitar bases de datos corruptas o registros huérfanos.

---

## Stack Tecnológico y Arquitectura

Este proyecto está construido sobre una arquitectura **MVC (Modelo-Vista-Controlador)** complementada con el patrón **DAO (Data Access Object)** para desacoplar completamente la interfaz gráfica de la base de datos.

* **Frontend:** Python + `Tkinter` (GUI) + `ttk` (Estilos y Treeviews).
* **Backend:** Python 3.x.
* **Base de Datos:** PostgreSQL (con llaves foráneas estrictas y llaves únicas compuestas).
* **Validación de Datos:** `Pydantic` (Validación de esquemas en la capa de negocio antes de tocar la BD).
* **Seguridad:** `bcrypt` para el manejo y encriptación de contraseñas de usuarios.

---

## Instalación y Configuración

Sigue estos pasos para desplegar el sistema en tu entorno local:

### 1. Clonar el repositorio
```bash
git clone [https://github.com/leandro291/sistema_hoteles.git](https://github.com/leandro291/sistema_hoteles.git)
cd sistema_hoteles
```
### 2. Crear y activar un entorno virtual

```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Mac/Linux:
source venv/bin/activate
```

### 3. Instalar dependencias
Instala las versiones exactas de las librerías necesarias ejecutando:

```bash
pip install -r requirements.txt
```

### 4. Configurar la Base de Datos

* Abre tu gestor de PostgreSQL (ej. pgAdmin o DBeaver).
* Crea una base de datos llamada hotel_db.
* Ejecuta el script database_schema.sql (incluido en la raíz del proyecto) para generar las tablas maestras, intermedias y sus restricciones de integridad.
* Ajusta las credenciales de conexión en el archivo config/database.py.

### 5. Ejecutar la aplicación

```bash
python main.py
```