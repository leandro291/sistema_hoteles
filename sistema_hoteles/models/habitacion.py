from typing import List
from pydantic import BaseModel

class HabitacionSchema(BaseModel):
    numero_piso: int
    numero_habitacion: int
    
class Habitacion:
    def __init__(self, numero_piso: int, numero_habitacion: int, id_tipo_habitacion: int, 
                 id_habitacion: int | None = None, estado: str = None):
        self.id_habitacion = id_habitacion

        self.numero_piso = numero_piso
        self.numero_habitacion = numero_habitacion
        self.estado = estado

        self.id_tipo_habitacion = id_tipo_habitacion
