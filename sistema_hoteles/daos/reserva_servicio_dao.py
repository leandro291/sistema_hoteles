from daos.base_dao import BaseDAO
from models.reserva_servicio import ReservaServicio

class ReservaServicioDAO(BaseDAO):

    def insertar_reserva_servicio(self, reserva_servicio: "ReservaServicio") -> bool:

        consulta = """
            INSERT INTO reserva_servicio (idservicio, idreserva, cantidad, subtotal)
            VALUES (%s, %s, %s, %s)
        """

        valores = (
            reserva_servicio.id_servicio,
            reserva_servicio.id_reserva,
            reserva_servicio.cantidad,
            reserva_servicio.subtotal
        )

        return self.insertar_sin_retorno_id(consulta, valores)