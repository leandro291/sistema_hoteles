from daos.base_dao import BaseDAO
from models.acompanante import Acompanante

class AcompananteDAO(BaseDAO):

    def insertar_acompanante(self, acompanante: "Acompanante") -> int:

        consulta = """
            INSERT INTO acompanante (nombre, apellido, dni, telefono, idreserva)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING idacompanante
        """

        valores = (
            acompanante.nombre,
            acompanante.apellido,
            acompanante.dni,
            acompanante.telefono,
            acompanante.id_reserva
        )

        return self.insertar_y_retornar_id(consulta, valores)
