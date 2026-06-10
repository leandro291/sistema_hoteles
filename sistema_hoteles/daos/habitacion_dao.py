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
    
    def obtener_precio_por_habitacion(self, id_habitacion: int):

        consulta = """
            SELECT th.precio
            FROM habitacion h
            JOIN tipo_habitacion th ON h.idhabitacion = th.idhabitacion
            WHERE h.idhabitacion = %s
        """

        valores = (id_habitacion,)

        cursor = self.conexion.cursor()

        try:
            cursor.execute(consulta, valores)
            resultado = cursor.fetchone()    

            if resultado is None:
                raise Exception("La habitacion no existe o no tiene un tipo asignado")
            
            return float(resultado[0])
        
        except Exception as e:
            raise e
        finally:
            cursor.close()