from daos.base_dao import BaseDAO
from models.servicio import Servicio

class ServicioDAO(BaseDAO):

    def insertar_servicio(self, servicio: "Servicio") -> int:
            
        consulta = """
            INSERT INTO servicio (nombre, descripcion, precio) 
            VALUES (%s, %s, %s)
            RETURNING id_servicio
        """

        valores = (
            servicio.nombre,
            servicio.descripcion,
            servicio.precio
        )

        return self.insertar_datos(consulta, valores)
    
    def obtener_todos_los_servicios(self):

        consulta = """
            SELECT 
                id_servicio,
                nombre,
                descripcion,
                precio
            FROM servicio
        """

        return self.obtener_datos(consulta)
    
    def obtener_precio_por_id(self, id_servicio: int) -> int:

        consulta = """
                SELECT precio 
                FROM servicio
                WHERE id_servicio = %s
            """
        
        valores = (id_servicio,)

        resultado = self.obtener_dato_por_id(consulta, valores)

        if resultado:
            return float(resultado[0])
            
        return 0.0 



