from daos.base_dao import BaseDAO
from models.pago import Pago

class PagoDAO(BaseDAO):

    def insertar_pago(self, pago: "Pago") -> int:

        consulta = """
            INSERT INTO pago (monto, fecha_pago, metodo_pago, estado_pago, tipo_comprobante, idreserva)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING idpago
        """

        valores = (
            pago.monto,
            pago.fecha_pago,
            pago.metodo_pago,
            pago.estado_pago,
            pago.tipo_comprobante,
            pago.id_reserva
        )

        return self.insertar_y_retornar_id(consulta, valores)
        
