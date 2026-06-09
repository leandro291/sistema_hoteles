from daos.base_dao import BaseDAO
from models.tipo_habitacion import TipoHabitacion

class TipoHabitacionDAO(BaseDAO):

    def insertar_tipo_habitacion(self, tipo_habitacion: "TipoHabitacion") -> int:

        consulta = """
            INSERT INTO tipo_habitacion (nombre, precio, capacidad)
            VALUES (%s, %s, %s)
            RETURNING idtipo_habitacion
        """

        valores = (
            tipo_habitacion.nombre,
            tipo_habitacion.precio,
            tipo_habitacion.capacidad
        )

        return self.insertar_y_retornar_id(consulta, valores)

