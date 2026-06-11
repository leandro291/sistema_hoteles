from datetime import date
from decimal import Decimal
from pydantic import BaseModel

class PagoSchema(BaseModel):
    monto: Decimal
    fecha_pago: date
    metodo_pago: str
    estado_pago: str
    tipo_comprobante: str

class Pago:
    def __init__(self, id_reserva: int, id_usuario: int, monto: Decimal, fecha_pago: date, metodo_pago: str, 
                 estado_pago: str, tipo_comprobante: str, id_pago: None = None):
        self.id_pago = id_pago

        self.monto = monto
        self.fecha_pago = fecha_pago
        self.metodo_pago = metodo_pago
        self.tipo_comprobante = tipo_comprobante
        self.estado_pago = estado_pago

        self.id_reserva = id_reserva
        self.id_usuario = id_usuario