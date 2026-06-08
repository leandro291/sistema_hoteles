from decimal import Decimal
from pydantic import BaseModel

class ServicioSchema(BaseModel):
    nombre: str
    descripcion: str
    precio: Decimal

class Servicio:
    def __init__(self, id_servicio: int, nombre: str, descripcion: str, precio: Decimal):
        self.id_servicio = id_servicio
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
    
