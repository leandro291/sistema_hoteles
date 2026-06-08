from pydantic import BaseModel

class UsuarioSchema(BaseModel):
    nombre: str
    apellido: str
    dni: str
    telefono: str
    correo: str
    direccion: str

class Usuario:
    def __init__(self, id_cliente: None, nombre: str, apellido: str, dni: str, telefono: str, correo: str, direccion: str):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.telefono = telefono
        self.correo = correo
        self.direccion = direccion
