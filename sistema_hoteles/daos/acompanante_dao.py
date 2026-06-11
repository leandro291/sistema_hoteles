from daos.base_dao import BaseDAO
from models.acompanante import Acompanante

class AcompananteDAO(BaseDAO):

    def insertar_acompanante(self, acompanante: "Acompanante") -> int:

        consulta = """
            INSERT INTO acompanante (nombre, apellido, tipo_documento, num_documento, telefono, id_reserva_habitacion)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id_acompanante
        """

        valores = (
            acompanante.nombre,
            acompanante.apellido,
            acompanante.tipo_documento,
            acompanante.numero_documento,
            acompanante.telefono,
            acompanante.id_reserva_habitacion
        )

        return self.insertar_datos(consulta, valores)
