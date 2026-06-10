from daos.base_dao import BaseDAO
from models.servicio import Servicio

class ServicioDAO(BaseDAO):

    def insertar_servicio(self, servicio: "Servicio") -> int:
            
        consulta = """
            INSERT INTO servicio (nombre, descripcion, precio) 
            VALUES (%s, %s, %s)
            RETURNING idservicio
        """

        valores = (
            servicio.nombre,
            servicio.descripcion,
            servicio.precio
        )

        return self.insertar_y_retornar_id(consulta, valores)
    
    def obtener_precio_por_id(self, id_servicio: int) -> int:

        consulta = """
                SELECT precio 
                FROM servicio
                WHERE idservicio = %s
            """
        
        valores = (id_servicio,)

        cursor = self.conexion.cursor()

        try:
            cursor.execute(consulta, valores)
            resultado = cursor.fetchone()    

            if resultado is None:
                raise Exception("El servicio no existe o no tiene un tipo asignado")
            
            return float(resultado[0])
        
        except Exception as e:
            raise e
        finally:
            cursor.close()



