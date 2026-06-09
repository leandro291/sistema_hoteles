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



