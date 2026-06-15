from typing import Tuple, Any
from daos.base_dao import BaseDAO
from models.tipo_habitacion import TipoHabitacion

class TipoHabitacionDAO(BaseDAO):

    def insertar_tipo_habitacion(self, tipo_habitacion: "TipoHabitacion") -> int:

        consulta = """
            INSERT INTO tipo_habitacion (nombre, precio, capacidad, descripcion)
            VALUES (%s, %s, %s, %s)
            RETURNING id_tipo_habitacion
        """

        valores = (
            tipo_habitacion.nombre,
            tipo_habitacion.precio,
            tipo_habitacion.capacidad,
            tipo_habitacion.descripcion
        )

        return self.insertar_datos(consulta, valores)
    
    def obtener_todos_los_tipos(self) -> Tuple[Any]:
        
        consulta = """
            SELECT id_tipo_habitacion, nombre
            FROM tipo_habitacion
        """

        return self.obtener_varios_datos(consulta)
    


