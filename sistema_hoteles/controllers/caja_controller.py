from config.database import ConexionDB
from datetime import datetime
from models.pago import Pago, PagoSchema
from daos.pago_dao import PagoDAO
from daos.reserva_dao import ReservaDAO
from daos.habitacion_dao import HabitacionDAO
from daos.reserva_servicio_dao import ReservaServicioDAO

from decimal import Decimal

class CajaController:
    def __init__(self):
        self.db = ConexionDB()

    def obtener_totales_liquidacion(self, id_reserva: int) -> tuple:

        conexion = self.db.obtener_conexion()

        try:
            dao_pago = PagoDAO(conexion)
            return dao_pago.obtener_totales_liquidacion(id_reserva)
        except Exception as e:
            raise Exception(f"Ha ocurrido un error en la BD: {e}")
        
    def registrar_pago_completo(self, id_reserva: int, monto: float, metodo: str, comprobante: str, id_usuario: int):
            
        conexion = self.db.obtener_conexion()

        try:
            dao_pago = PagoDAO(conexion)
            
            nuevo_pago = Pago(
                id_reserva=id_reserva,
                id_usuario=id_usuario,
                monto=Decimal(str(monto)), 
                metodo_pago=metodo,
                estado_pago='Completado',  
                tipo_comprobante=comprobante
            )
            
            dao_pago.registrar_transaccion_pago(nuevo_pago)
            
        except Exception as e:
            raise Exception(f"Fallo en la caja registradora: {e}")


    def obtener_todos_los_pagos(self) -> list:
        conexion = None
        try:
            conexion = self.db.obtener_conexion()
            dao_pago = PagoDAO(conexion) 
            
            registros = dao_pago.obtener_historial_pagos()
            
            return registros if registros else []
            
        except Exception as e:
            raise Exception(f"Fallo al obtener historial: {e}")


