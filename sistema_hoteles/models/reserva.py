from datetime import date
from decimal import Decimal
from pydantic import BaseModel

class ReservaSchema(BaseModel):
    fecha_reserva: date
    fecha_entrada: date
    fecha_salida: date
    cantidad_huesped: int
    estado_reserva: str
    total: Decimal

class Reserva:
    def __init__(self, id_reserva: None, fecha_reserva: date, fecha_entrada: date, fecha_salida: date, cantidad_huesped: int, estado_reserva: str, total: Decimal):
        self.id_reserva = id_reserva
        self.fecha_reserva = fecha_reserva
        self.fecha_entrada = fecha_entrada
        self.fecha_salida = fecha_salida
        self.cantidad_huesped = cantidad_huesped
        self.estado_reserva = estado_reserva
        self.total = total
