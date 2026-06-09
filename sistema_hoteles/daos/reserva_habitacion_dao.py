from daos.base_dao import BaseDAO
from models.reserva_habitacion import ReservaHabitacion

class ReservaHabitacionDAO(BaseDAO):

    def insertar_reserva_habitacion(self, reserva_habitacion: "ReservaHabitacion") -> bool:
        
        consulta = """
            INSERT INTO reserva_habitacion (idreserva, idhabitacion)
            VALUES (%s, %s)
        """

        valores = (
            reserva_habitacion.id_reserva,
            reserva_habitacion.id_habitacion
        )

        return self.insertar_sin_retorno_id(consulta, valores)