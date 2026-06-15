from daos.base_dao import BaseDAO
from models.reserva_habitacion import ReservaHabitacion

class ReservaHabitacionDAO(BaseDAO):

    def insertar_reserva_habitacion(self, reserva_habitacion: "ReservaHabitacion") -> int:
        
        consulta = """
            INSERT INTO reserva_habitacion (id_habitacion, id_reserva, precio_x_noche, es_titular, subtotal)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_reserva_habitacion
        """

        valores = (
            reserva_habitacion.id_habitacion,
            reserva_habitacion.id_reserva,
            reserva_habitacion.precio_por_noche,
            reserva_habitacion.es_titular,
            reserva_habitacion.subtotal
        )

        return self.insertar_datos(consulta, valores)