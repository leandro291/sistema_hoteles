from decimal import Decimal

class ReservaServicio:
    def __init__(self, id_servicio: int, id_reserva: int, precio_unitario: Decimal, cantidad: int, 
                 subtotal: Decimal, id_reserva_servicio: None = None):
        self.id_reserva_servicio = id_reserva_servicio

        self.precio_unitario = precio_unitario
        self.cantidad = cantidad
        self.subtotal = subtotal

        self.id_servicio = id_servicio    
        self.id_reserva = id_reserva      

