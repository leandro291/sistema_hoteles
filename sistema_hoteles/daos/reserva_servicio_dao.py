from typing import Tuple, Any
from daos.base_dao import BaseDAO
from models.reserva_servicio import ReservaServicio

class ReservaServicioDAO(BaseDAO):

    def insertar_reserva_servicio(self, reserva_servicio: "ReservaServicio") -> int:

        consulta = """
            INSERT INTO reserva_servicio (id_servicio, id_reserva, precio_unitario, cantidad, subtotal)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_reserva_servicio
        """

        valores = (
            reserva_servicio.id_servicio,
            reserva_servicio.id_reserva,
            reserva_servicio.precio_unitario,
            reserva_servicio.cantidad,
            reserva_servicio.subtotal
        )

        return self.insertar_datos(consulta, valores)
    
    def obtener_consumos_por_reserva(self, id_reserva: int) -> Tuple[Any]:

        consulta = """
            SELECT 
                rs.id_reserva_servicio, 
                s.nombre,                
                rs.precio_unitario,      
                rs.cantidad,             
                rs.subtotal              
            FROM reserva_servicio rs
            JOIN servicio s ON rs.id_servicio = s.id_servicio
            WHERE rs.id_reserva = %s;
        """
        
        return self.obtener_varios_datos_por_id(consulta, id_reserva)

    def eliminar_consumo(self, id_reserva_servicio: int) -> None:
        consulta = "DELETE FROM reserva_servicio WHERE id_reserva_servicio = %s;"
        self.eliminar_dato_por_id(consulta, id_reserva_servicio)
