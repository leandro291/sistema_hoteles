from daos.base_dao import BaseDAO
from models.pago import Pago

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
        
