from pydantic import BaseModel

class AcompananteSchema(BaseModel):
    nombre: str
    apellido: str
    dni: str
    edad: int

class Acompanante:
    def __init__(self, id_acompanante: None, nombre: str, apellido: str, dni: str, edad: int):
        self.id_acompanante = id_acompanante
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.edad = edad
