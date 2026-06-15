from decimal import Decimal
from pydantic import BaseModel, Field

class ServicioSchema(BaseModel):
    nombre: str
    descripcion: str
    precio: Decimal = Field(gt=0)

    

class Servicio:
    def __init__(self, nombre: str, descripcion: str, precio: Decimal, id_servicio: None = None):
        self.id_servicio = id_servicio
        
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio

    
