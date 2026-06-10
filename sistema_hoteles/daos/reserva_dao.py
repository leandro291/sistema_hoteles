from daos.base_dao import BaseDAO
from models.reserva import Reserva

class ReservaDAO(BaseDAO):

    def insertar_reserva(self, reserva: "Reserva") -> int:

        consulta = """
            INSERT INTO reserva (fecha_reserva, fecha_entrada, fecha_salida, cantidad_huespedes, estado_reserva, total, id_cliente)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING idreserva
        """

        valores = (
            reserva.fecha_reserva,
            reserva.fecha_entrada,
            reserva.fecha_salida,
            reserva.cantidad_huesped,
            reserva.estado_reserva,
            reserva.total,
            reserva.id_cliente
        )

        return self.insertar_y_retornar_id(consulta, valores)
    
    def cambiar_estado_reserva(self, id_reserva: int, nuevo_estado: str) -> bool:
        
        consulta = """
            UPDATE reserva SET estado_reserva = %s WHERE idreserva = %s
        """

        valores = (nuevo_estado, id_reserva)

        self.cambiar_estado(consulta, valores)
    
    def obtener_total_reserva(self, id_reserva: int) -> float:

        consulta = """
            SELECT total
            FROM reserva
            WHERE idreserva = %s
        """

        valores = (id_reserva,)

        cursor = self.conexion.cursor()

        try:

            cursor.execute(consulta, valores)
            resultado = cursor.fetchone()

            if not resultado:
                raise Exception("No se ha eonctrado valor para el ID ingresado")
            
            return float(resultado[0])

        except Exception as e:
            raise e
        finally:
            cursor.close()
