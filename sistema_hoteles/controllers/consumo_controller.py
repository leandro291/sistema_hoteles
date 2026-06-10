from config.database import ConexionDB

from models.reserva_servicio import ReservaServicio

from daos.servicio_dao import ServicioDAO
from daos.reserva_servicio_dao import ReservaServicioDAO


class ConsumoController:
    def __init__(self):
        self.db = ConexionDB()

    def registrar_servicio(self, id_servicio: int, id_reserva: int, cantidad: int ) -> None:

        if cantidad <= 0:
            raise Exception("La cantidad ingresada no puede ser menor o igual a 0")

        conexion = self.db.obtener_conexion()

        try:

            dao_servicio = ServicioDAO(conexion)

            precio_servicio = dao_servicio.obtener_precio_por_id(id_servicio)
            subtotal = cantidad * precio_servicio

            reserva_servicio = ReservaServicio(id_servicio, id_reserva, cantidad, subtotal)
            dao_reserva_servicio = ReservaServicioDAO(conexion)
            dao_reserva_servicio.insertar_reserva_servicio(reserva_servicio)

            conexion.commit()

        except Exception as e:
            conexion.rollback()
            raise Exception(f"Ha ocurrido un error en la Base de Datos: {e}")
        
    def anular_servicio(self, id_reserva: int, id_servicio):

        conexion = self.db.obtener_conexion()
        try:

            dao_reserva_servicio = ReservaServicioDAO(conexion)
            dao_reserva_servicio.eliminar_reserva_servicio(id_servicio, id_reserva)

            conexion.commit()

        except Exception as e:
            conexion.rollback()
            raise Exception(f"Ha ocurrido un error en la Base de Datos: {e}")
        