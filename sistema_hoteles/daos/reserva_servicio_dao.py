from daos.base_dao import BaseDAO
from models.reserva_servicio import ReservaServicio

class ReservaServicioDAO(BaseDAO):

    def insertar_reserva_servicio(self, reserva_servicio: "ReservaServicio") -> bool:

        consulta = """
            INSERT INTO reserva_servicio (idservicio, idreserva, cantidad, subtotal)
            VALUES (%s, %s, %s, %s)
        """

        valores = (
            reserva_servicio.id_servicio,
            reserva_servicio.id_reserva,
            reserva_servicio.cantidad,
            reserva_servicio.subtotal
        )

        return self.insertar_sin_retorno_id(consulta, valores)
    
    def eliminar_reserva_servicio(self, id_servicio: int, id_reserva: int):

        cursor = self.conexion.cursor()
        
        consulta = """
            DELETE FROM reserva_servicio 
            WHERE idservicio = %s AND idreserva = %s
        """

        valores = (id_servicio, id_reserva)

        try:

            cursor.execute(consulta, valores)
            
            if cursor.rowcount == 0:
                raise Exception("No se encontró el registro para eliminar")

        except Exception as e:
            raise e
        finally:
            cursor.close()
