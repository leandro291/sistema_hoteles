from pydantic import BaseModel, Field
from decimal import Decimal


class TipoHabitacionSchema(BaseModel):
    nombre: str
    precio: Decimal = Field(gt=0)
    capacidad: int = Field(gt=0)
    descripcion: str


class TipoHabitacion:
    def __init__(self, nombre: str, precio: Decimal, capacidad: int, descripcion: str, id_tipo_habitacion: int | None = None):
        self.id_tipo_habitacion = id_tipo_habitacion
        
        self.nombre = nombre
        self.precio = precio
        self.capacidad = capacidad
        self.descripcion = descripcion

    def __str__(self):
        return f"TipoHabitacion(id={self.id_tipo_habitacion}, nombre='{self.nombre}', capacidad={self.capacidad})"
