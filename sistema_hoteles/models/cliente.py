from pydantic import BaseModel
from typing import List

class ClienteSchema(BaseModel):
    nombre: str
    apellido: str
    dni: str
    telefono: str
    correo: str
    direccion: str

class Cliente:
    def __init__(self, id_cliente: int | None, nombre: str, apellido: str, dni: str, telefono: str, correo: str, direccion: str):
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.telefono = telefono
        self.correo = correo
        self.direccion = direccion

        self.reservas = List[int] = []
