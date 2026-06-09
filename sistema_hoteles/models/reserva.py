from typing import List
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
    def __init__(self, id_cliente: int, fecha_reserva: date, fecha_entrada: date, fecha_salida: date, cantidad_huesped: int, estado_reserva: str, total: Decimal, id_reserva: None=None):
        self.id_reserva = id_reserva
        self.id_cliente = id_cliente
        self.fecha_reserva = fecha_reserva
        self.fecha_entrada = fecha_entrada
        self.fecha_salida = fecha_salida
        self.cantidad_huesped = cantidad_huesped
        self.estado_reserva = estado_reserva
        self.total = total

        self.pagos: List[int] = []
        self.acompanantes: List[int] = []
        self.reserva_servicio: List[int] = []
        self.reserva_habitacion: List[int] = []

        
