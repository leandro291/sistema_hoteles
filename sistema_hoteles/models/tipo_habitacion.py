from pydantic import BaseModel, Field
from decimal import Decimal
from typing import List

class TipoHabitacionSchema(BaseModel):
    nombre: str
    precio: Decimal = Field(gt=0)
    capacidad: int = Field(gt=0)
    descripcion: str

class TipoHabitacion:
    def __init__(self, nombre: str, precio: Decimal, capacidad: int, descripcion: str, id_tipo_habitacion: None = None):
        self.id_tipo_habitacion = id_tipo_habitacion
        
        self.nombre = nombre
        self.precio = precio
        self.capacidad = capacidad
        self.descripcion = descripcion



