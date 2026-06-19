from decimal import Decimal


class ReservaHabitacion:
    def __init__(self, id_habitacion: int, id_reserva: int, precio_por_noche: Decimal, 
                 es_titular: bool, subtotal: Decimal, id_reserva_habitacion: int | None = None):
        self.id_reserva_habitacion = id_reserva_habitacion

        self.precio_por_noche = precio_por_noche
        self.es_titular = es_titular
        self.subtotal = subtotal

        self.id_habitacion = id_habitacion
        self.id_reserva = id_reserva

    def __str__(self):
        return f"ReservaHabitacion(id={self.id_reserva_habitacion}, habitacion={self.id_habitacion}, reserva={self.id_reserva})"