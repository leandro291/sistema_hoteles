from models.pago import Pago
from daos.base_dao import BaseDAO

class PagoDAO(BaseDAO):

    def insertar_pago(self, pago: "Pago") -> int:

        consulta = """
            INSERT INTO pago (monto, metodo_pago, tipo_comprobante, estado_pago, id_reserva, id_usuario)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id_pago
        """

        valores = (
            pago.monto,
            pago.metodo_pago,
            pago.tipo_comprobante,
            pago.estado_pago,
            pago.id_reserva,
            pago.id_usuario
        )

        return self.insertar_datos(consulta, valores)
    
    def obtener_totales_liquidacion(self, id_reserva: int) -> tuple:
        consulta = """

            SELECT 
                r.id_reserva,
                CONCAT(c.nombre, ' ', c.apellido) AS cliente,
                
                COALESCE((SELECT SUM(subtotal) FROM reserva_habitacion WHERE id_reserva = r.id_reserva), 0.00) AS costo_cuarto, 
                COALESCE((SELECT SUM(subtotal) FROM reserva_servicio WHERE id_reserva = r.id_reserva), 0.00) AS costo_extras,                
                COALESCE((SELECT SUM(subtotal) FROM reserva_habitacion WHERE id_reserva = r.id_reserva), 0.00) + 
                COALESCE((SELECT SUM(subtotal) FROM reserva_servicio WHERE id_reserva = r.id_reserva), 0.00) AS total_a_pagar
                
            FROM reserva r
            JOIN cliente c ON r.id_cliente = c.id_cliente
            WHERE r.id_reserva = %s;
        """
        return self.obtener_un_dato_por_id(consulta, id_reserva)

    def obtener_historial_pagos(self) -> list:
        consulta = """
            SELECT 
                p.id_pago,
                TO_CHAR(p.fecha_pago, 'DD-MM-YYYY HH24:MI') AS fecha_pago,
                CONCAT('Hab. ', h.num_habitacion, ' - ', c.nombre, ' ', c.apellido) AS reserva_cliente,
                p.monto,
                p.metodo_pago,
                p.tipo_comprobante,
                p.estado_pago,
                u.nombre_usuario
            FROM pago p
            JOIN reserva r ON p.id_reserva = r.id_reserva
            JOIN cliente c ON r.id_cliente = c.id_cliente
            JOIN reserva_habitacion rh ON r.id_reserva = rh.id_reserva
            JOIN habitacion h ON rh.id_habitacion = h.id_habitacion
            JOIN usuario u ON p.id_usuario = u.id_usuario
            ORDER BY p.fecha_pago DESC;
        """
        return self.obtener_varios_datos(consulta)



        
