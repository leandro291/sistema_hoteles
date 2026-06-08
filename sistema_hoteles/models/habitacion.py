from pydantic import BaseModel

class HabitacionSchema(BaseModel):
    numero_piso: int
    numero_habitacion: int
    estado: str


class Habitacion:
    def __init__(self, id_habitacion: int | None, numero_piso: int, numero_habitacion: int, estado: str, tipo_habitacion: int):
        self.id_habitacion = id_habitacion
        self.numero_piso = numero_piso
        self.numero_habitacion = numero_habitacion
        self.estado = estado
        self.tipo_habitacion = tipo_habitacion