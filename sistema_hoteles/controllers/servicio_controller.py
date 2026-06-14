from config.database import ConexionDB
from decimal import Decimal
from pydantic import ValidationError

from models.servicio import Servicio, ServicioSchema
from daos.servicio_dao import ServicioDAO
from daos.reserva_dao import ReservaDAO

class ServicioController:
    def __init__(self):
        self.db = ConexionDB()

    def registrar_nuevo_servicio(self, nombre: str, descripcion: str, precio: str):

        precio_formateado = Decimal(precio)

        try:

            validador_servicio = ServicioSchema(
                nombre=nombre,
                descripcion=descripcion,
                precio=precio_formateado
            )

        except ValidationError as e:
            raise ValueError(f"Dato invalido para el servicio: {e}")
        
        
        servicio = Servicio(
            nombre=validador_servicio.nombre,
            descripcion=validador_servicio.descripcion,
            precio=validador_servicio.precio
        )

        conexion = self.db.obtener_conexion()

        try:
            
            dao_servicio = ServicioDAO(conexion)
            return dao_servicio.insertar_servicio(servicio)

        except Exception as e:
            raise Exception(f"Ha ocurrido un error en la BD: {e}")

    def obtener_todos_los_servicios(self):

        conexion = self.db.obtener_conexion()

        try:

            dao_servicio = ServicioDAO(conexion)
            return dao_servicio.obtener_todos_los_servicios()
        
        except Exception as e:
            raise Exception(f"Ha ocurrido un error en la BD: {e}")
        
    def obtener_todas_las_reservas_en_curso(self):

        conexion = self.db.obtener_conexion()

        try:

            dao_reserva = ReservaDAO(conexion)
            return dao_reserva.obtener_reservas_en_curso()
        
        except Exception as e:
            raise Exception(f"Ha ocurrido un error en la BD: {e}")
