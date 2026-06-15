from typing import Tuple, Any
from daos.base_dao import BaseDAO
from models.reserva import Reserva

class ReservaDAO(BaseDAO):

    def insertar_reserva(self, reserva: "Reserva") -> int:

        consulta = """
            INSERT INTO reserva (fecha_entrada, fecha_salida, estado_reserva, id_cliente, id_usuario)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_reserva
        """

        valores = (
            reserva.fecha_entrada,
            reserva.fecha_salida,
            reserva.estado_reserva,
            reserva.id_cliente,
            reserva.id_usuario
        )

        return self.insertar_datos(consulta, valores)
    
    def cambiar_estado_reserva(self, id_reserva: int, nuevo_estado: str) -> None:
        
        consulta = """
            UPDATE reserva SET estado_reserva = %s WHERE id_reserva = %s
        """

        valores = (nuevo_estado, id_reserva)

        self.cambiar_estado(consulta, valores)

    def obtener_reservas_en_curso(self) -> Tuple[Any]:

        consulta = """
            SELECT 
                r.id_reserva, 
                h.num_habitacion, 
                c.nombre, 
                c.apellido
            FROM reserva r
            JOIN cliente c ON r.id_cliente = c.id_cliente
            JOIN reserva_habitacion rh ON r.id_reserva = rh.id_reserva
            JOIN habitacion h ON rh.id_habitacion = h.id_habitacion
            WHERE r.estado_reserva = 'En curso';
        """

        return self.obtener_varios_datos(consulta)
    
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
