from decimal import Decimal
from pydantic import ValidationError
from config.database import ConexionDB

from models.pago import Pago, PagoSchema
from daos.pago_dao import PagoDAO
from daos.reserva_dao import ReservaDAO
from daos.habitacion_dao import HabitacionDAO


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
            
        try:
            validador_pago = PagoSchema(
                monto=Decimal(str(monto)),
                metodo_pago=metodo,
                estado_pago="Completado",
                tipo_comprobante=comprobante
            )
        except ValidationError as e:
            raise ValueError(f"Ha ocurrido un error al registrar datos del pago: {e}")
        
        conexion = self.db.obtener_conexion()

        try:
            dao_pago = PagoDAO(conexion)
            dao_reserva = ReservaDAO(conexion)
            dao_habitacion = HabitacionDAO(conexion)
            
            nuevo_pago = Pago(
                id_reserva=id_reserva,
                id_usuario=id_usuario,
                monto=validador_pago.monto, 
                metodo_pago=validador_pago.metodo_pago,
                estado_pago=validador_pago.estado_pago,  
                tipo_comprobante=validador_pago.tipo_comprobante
            )
            
            dao_pago.insertar_pago(nuevo_pago)
            dao_reserva.cambiar_estado_reserva(id_reserva, "Finalizado")
            dao_habitacion.cambiar_estado_por_reserva(id_reserva)
            
        except Exception as e:
            raise Exception(f"Ha ocurrido un error en la BD: {e}")


    def obtener_todos_los_pagos(self) -> list:

        conexion = self.db.obtener_conexion()

        try:
            dao_pago = PagoDAO(conexion) 
            
            registros = dao_pago.obtener_historial_pagos()
            
            return registros if registros else []
            
        except Exception as e:
            raise Exception(f"Fallo al obtener historial: {e}")


