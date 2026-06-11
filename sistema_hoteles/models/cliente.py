from typing import List
from pydantic import BaseModel

class ClienteSchema(BaseModel):
    nombre: str
    apellido: str
    dni: str
    telefono: str
    correo: str
    direccion: str

class Cliente:
    def __init__(self, nombre: str, apellido: str, dni: str, telefono: str, correo: str, direccion: str, id_cliente: None = None):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.telefono = telefono
        self.correo = correo
        self.direccion = direccion
