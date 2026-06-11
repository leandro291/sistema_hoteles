from typing import List
from datetime import date
from decimal import Decimal
from pydantic import BaseModel

class ReservaSchema(BaseModel):
    fecha_entrada: date
    fecha_salida: date

class Reserva:
    def __init__(self, id_cliente: int, id_usuario: int, fecha_entrada: date, fecha_salida: date, 
                 estado_reserva: str, id_reserva: None=None):
        self.id_reserva = id_reserva
        
        self.fecha_entrada = fecha_entrada
        self.fecha_salida = fecha_salida
        self.estado_reserva = estado_reserva

        self.id_usuario = id_usuario
        self.id_cliente = id_cliente


        
