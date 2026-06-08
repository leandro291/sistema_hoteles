from pydantic import BaseModel
from decimal import Decimal
from typing import List

class TipoHabitacionSchema(BaseModel):
    nombre: str
    precio : Decimal
    capacidad: int

class TipoHabitacion:
    def __init__(self, id_tipo_habitacion: None, nombre: str, precio: Decimal, capacidad: int):
        self.id_tipo_habitacion = id_tipo_habitacion
        self.nombre = nombre
        self.precio = precio
        self.capacidad = capacidad
        self.habitaciones: List[int] = []



