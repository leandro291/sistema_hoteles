from decimal import Decimal
from pydantic import BaseModel

class ReservaServicioSchema(BaseModel):
    cantidad: int
    subtotal: Decimal

class ReservaServicio:
    def __init__(self, id_servicio: int, id_reserva: int, cantidad: int, subtotal: Decimal):
        self.id_servicio = id_servicio    
        self.id_reserva = id_reserva      
        self.cantidad = cantidad
        self.subtotal = subtotal

