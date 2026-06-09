from daos.base_dao import BaseDAO
from models.reserva import Reserva

class ReservaDAO(BaseDAO):

    def insertar_reserva(self, reserva: "Reserva") -> int:

        consulta = """
            INSERT INTO reserva (fecha_reserva, fecha_entrada, fecha_salida, cantidad_huespedes, estado_reserva, total, id_cliente)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING idreserva
        """

        valores = (
            reserva.fecha_reserva,
            reserva.fecha_entrada,
            reserva.fecha_salida,
            reserva.cantidad_huesped,
            reserva.estado_reserva,
            reserva.total,
            reserva.id_cliente
        )

        return self.insertar_y_retornar_id(consulta, valores)