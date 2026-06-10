from config.database import ConexionDB

from datetime import datetime

from models.pago import Pago, PagoSchema

from daos.pago_dao import PagoDAO
from daos.reserva_dao import ReservaDAO
from daos.habitacion_dao import HabitacionDAO
from daos.reserva_servicio_dao import ReservaServicioDAO

class CajaController:
    def __init__(self):
        self.db = ConexionDB()

    def obtener_cuenta_final(self, id_reserva: int) -> float:

        try: 
            conexion = self.db.obtener_conexion()

            dao_reserva = ReservaDAO(conexion)
            total_estadia = dao_reserva.obtener_total_reserva(id_reserva)

            dao_reserva_servicio = ReservaServicioDAO(conexion)
            total_consumos = dao_reserva_servicio.obtener_total_consumo(id_reserva)

            return total_estadia + total_consumos
        
        except Exception as e:
            conexion.rollback()
            raise Exception(f"Ha ocurrido un error en la Base de Datos: {e}")
        
    
    def finalizar_reserva(self, id_reserva: int, id_habitacion: int, metodo_pago: str, tipo_comprobante: str) -> None:
            
        try:
            
            conexion = self.db.obtener_conexion()
            total_pago = self.obtener_cuenta_final(id_reserva)
            fecha_actual = datetime.now()

            validador_pago = PagoSchema(
                monto=total_pago,
                fecha_pago=fecha_actual,
                metodo_pago=metodo_pago,
                tipo_comprobante=tipo_comprobante
            )

            nuevo_pago = Pago(
                id_reserva=id_reserva,
                monto=validador_pago.monto,
                fecha_pago=validador_pago.fecha_pago,
                metodo_pago=validador_pago.metodo_pago,
                tipo_comprobante=validador_pago.tipo_comprobante
            )

            dao_pago = PagoDAO(conexion)
            dao_pago.insertar_pago(nuevo_pago)

            dao_habitacion = HabitacionDAO(conexion)
            dao_habitacion.cambiar_estado_habitacion(id_habitacion, "Disponible")

            dao_reserva = ReservaDAO(conexion)
            dao_reserva.cambiar_estado_reserva(id_reserva, "Finalizada")

            conexion.commit()
        

        except Exception as e:
            conexion.rollback()
            raise Exception(f"Ha ocurrido un error en la Base de Datos: {e}")