from daos.base_dao import BaseDAO
from models.habitacion import Habitacion

class HabitacionDAO(BaseDAO):
    
    def insertar_habitacion(self, habitacion: "Habitacion") -> int:

        consulta = """
            INSERT INTO habitacion (num_piso, num_habitacion, estado, idtipo_habitacion)
            VALUES (%s, %s, %s, %s)
            RETURNING idhabitacion
        """

        valores = (
            habitacion.numero_piso,
            habitacion.numero_habitacion,
            habitacion.estado,
            habitacion.id_tipo_habitacion
        )

        return self.insertar_y_retornar_id(consulta, valores)
    