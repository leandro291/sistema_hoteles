from pydantic import BaseModel

class AcompananteSchema(BaseModel):
    nombre: str
    apellido: str
    tipo_documento: str
    numero_documento: str
    edad: int

class Acompanante:
    def __init__(self, id_reserva_habitacion: int, nombre: str, apellido: str, telefono: str, 
                 tipo_documento: str, numero_documento: str, id_acompanante: None = None):
        self.id_acompanante = id_acompanante

        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.tipo_documento = tipo_documento
        self.numero_documento = numero_documento

        self.id_reserva_habitacion = id_reserva_habitacion



