from datetime import date
from pydantic import BaseModel, model_validator


class ReservaSchema(BaseModel):
    fecha_entrada: date
    fecha_salida: date

    @model_validator(mode='after')
    def validar_fechas(self):
        if self.fecha_salida <= self.fecha_entrada:
            raise ValueError("La fecha de salida debe ser posterior a la fecha de entrada")
        return self


class Reserva:
    def __init__(self, id_cliente: int, id_usuario: int, fecha_entrada: date, fecha_salida: date, 
                 estado_reserva: str, id_reserva: int | None = None):
        self.id_reserva = id_reserva
        
        self.fecha_entrada = fecha_entrada
        self.fecha_salida = fecha_salida
        self.estado_reserva = estado_reserva

        self.id_usuario = id_usuario
        self.id_cliente = id_cliente

    def __str__(self):
        return f"Reserva(id={self.id_reserva}, entrada={self.fecha_entrada}, salida={self.fecha_salida})"
