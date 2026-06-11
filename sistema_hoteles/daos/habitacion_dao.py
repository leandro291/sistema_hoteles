from daos.base_dao import BaseDAO
from models.habitacion import Habitacion

class HabitacionDAO(BaseDAO):
    
    def insertar_habitacion(self, habitacion: "Habitacion") -> int:

        consulta = """
            INSERT INTO habitacion (num_piso, num_habitacion, estado, id_tipo_habitacion)
            VALUES (%s, %s, %s, %s)
            RETURNING id_habitacion
        """

        valores = (
            habitacion.numero_piso,
            habitacion.numero_habitacion,
            habitacion.estado,
            habitacion.id_tipo_habitacion
        )

        return self.insertar_datos(consulta, valores)
    
    def cambiar_estado_habitacion(self, id_habitacion: int, nuevo_estado: str) -> bool:
        
        consulta = """
            UPDATE habitacion SET estado = %s WHERE idhabitacion = %s
        """

        valores = (nuevo_estado, id_habitacion)

        self.cambiar_estado(consulta, valores)
        
    def obtener_precio_por_habitacion(self, id_habitacion: int) -> float:

        consulta = """
            SELECT th.precio
            FROM habitacion h
            JOIN tipo_habitacion th ON h.id_habitacion = th.id_habitacion
            WHERE h.idhabitacion = %s
        """

        valores = (id_habitacion,)

        return float(self.obtener_dato_por_id(consulta, valores))
    
    def obtener_cantidad_por_habitacion(self, id_habitacion: int) -> int:

        consulta = """
            SELECT th.cantidad
            FROM habitacion h
            JOIN tipo_habitacion th ON h.id_habitacion = th.id_habitacion
            WHERE h.idhabitacion = %s
        """

        valores = (id_habitacion)

        return int(self.obtener_dato_por_id(self,id_habitacion))