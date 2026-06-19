from pydantic import BaseModel, field_validator


class AcompananteSchema(BaseModel):
    nombre: str
    apellido: str
    tipo_documento: str
    numero_documento: str
    telefono: str

    @field_validator('nombre', 'apellido')
    @classmethod
    def validate_no_numeros(cls, valor: str) -> str:
        if any(char.isdigit() for char in valor):
            raise ValueError("El nombre y el apellido no deben contener números.")
        return valor

    @field_validator('telefono')
    @classmethod
    def validate_telefono(cls, valor: str) -> str:
        if len(valor) != 9 or not valor.isdigit():
            raise ValueError("El teléfono debe tener exactamente 9 dígitos.")
        return valor
    
    @field_validator('numero_documento')
    @classmethod
    def validate_numero_documento(cls, valor: str) -> str:
        if not valor.isdigit():
            raise ValueError(f"El Numero de Documento {valor} debe estar formado de dígitos")
        return valor


class Acompanante:
    def __init__(self, id_reserva_habitacion: int, nombre: str, apellido: str, 
                 tipo_documento: str, numero_documento: str, telefono: str, id_acompanante: int | None = None):
        self.id_acompanante = id_acompanante

        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.tipo_documento = tipo_documento
        self.numero_documento = numero_documento

        self.id_reserva_habitacion = id_reserva_habitacion

    def __str__(self):
        return f"Acompanante(id={self.id_acompanante}, nombre='{self.nombre}', apellido='{self.apellido}')"
