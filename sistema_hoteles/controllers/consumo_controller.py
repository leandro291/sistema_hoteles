from config.database import ConexionDB
from typing import Tuple, Any

from models.reserva_servicio import ReservaServicio

from daos.servicio_dao import ServicioDAO
from daos.reserva_servicio_dao import ReservaServicioDAO

class ConsumoController:
    def __init__(self):
        self.db = ConexionDB()

    def registrar_servicio(self, id_servicio: int, id_reserva: int, cantidad: int ) -> int:

        if cantidad <= 0:
            raise Exception("La cantidad ingresada no puede ser menor o igual a 0")

        conexion = self.db.obtener_conexion()

        try:

            dao_servicio = ServicioDAO(conexion)
            precio_servicio = dao_servicio.obtener_precio_por_id(id_servicio)

            if precio_servicio is None:
                raise ValueError("El servicio seleccionado no existe o no tiene precio válido.")

            subtotal = cantidad * precio_servicio

            reserva_servicio = ReservaServicio(
                id_servicio=id_servicio,
                id_reserva=id_reserva,
                precio_unitario=precio_servicio,
                cantidad=cantidad,
                subtotal=subtotal,
            )

            dao_reserva_servicio = ReservaServicioDAO(conexion)
            id_generado_reserva_servicio =dao_reserva_servicio.insertar_reserva_servicio(reserva_servicio)

            return id_generado_reserva_servicio

        except Exception as e:
            raise Exception(f"Ha ocurrido un error en la base de datos: {e}")
                
    def obtener_historial_consumos(self, id_reserva: int) -> Tuple[Any]:

        conexion = self.db.obtener_conexion()

        try:
            dao_rs = ReservaServicioDAO(conexion) 
            return dao_rs.obtener_consumos_por_reserva(id_reserva)
            
        except Exception as e:
            raise Exception(f"Fallo al leer historial de BD: {e}")

    def eliminar_consumo(self, id_reserva_servicio: int) -> None:

        conexion = self.db.obtener_conexion()

        try:
            dao_rs = ReservaServicioDAO(conexion)
            dao_rs.eliminar_consumo(id_reserva_servicio)
            
        except Exception as e:
            raise Exception(f"Fallo al leer historial de BD: {e}")