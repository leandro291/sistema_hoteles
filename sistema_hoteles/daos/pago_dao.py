from config.database import ConexionDB
from models.pago import Pago

class PagoDAO:
    def __init__(self):
        self.db = ConexionDB()
        self.conexion = self.db.obtener_conexion()

    def insertar_pago(self, pago: "Pago") -> int:

        cursor = self.conexion.cursor()

        try:

            consulta = """
                INSERT INTO pago (monto, fecha_pago, metodo_pago, estado_pago, tipo_comprobante, idreserva)
                VALUES (%s, %s, %s, %s, %s, %s,)
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

            cursor.execute(consulta, valores)
            id_obtenido = cursor.fetchone()[0]
            self.conexion.commit()

            return id_obtenido

        except Exception as e:
            self.conexion.rollback()
            raise e
        finally:
            if cursor:
                cursor.close()
        
