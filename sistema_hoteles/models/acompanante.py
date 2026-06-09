from pydantic import BaseModel

class AcompananteSchema(BaseModel):
    nombre: str
    apellido: str
    dni: str
    edad: int

class Acompanante:
    def __init__(self, id_reserva: int, nombre: str, apellido: str, dni: str, edad: int, id_acompanante: None = None):
        self.id_acompanante = id_acompanante
        self.id_reserva = id_reserva
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.edad = edad



