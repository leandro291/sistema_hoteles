from config.database import ConexionDB

from models.cliente import Cliente
from models.reserva import Reserva
from models.acompanante import Acompanante
from models.reserva_habitacion import ReservaHabitacion

from daos.cliente_dao import ClienteDAO
from daos.reserva_dao import ReservaDAO
from daos.habitacion_dao import HabitacionDAO
from daos.reserva_habitacion_dao import ReservaHabitacionDAO
from daos.acompanante_dao import AcompananteDAO

from datetime import datetime
from typing import List

class RecepcionController:
    def __init__(self):
        self.db = ConexionDB()

    def registrar_check_in(self, cliente: "Cliente", reserva: "Reserva", id_habitacion: int, acompanantes: List["Acompanante"]):

        # Logica para obtener las fechas para la reserva
        fecha_entrada = datetime.strptime(reserva.fecha_entrada, "%Y-%m-%d")
        fecha_salida = datetime.strptime(reserva.fecha_salida, "%Y-%m-%d")
        noches_totales = (fecha_salida - fecha_entrada).days

        if noches_totales <= 0:
            raise ValueError("La fecha de salida debe ser mayor a la de entrada")
        
        conexion = self.db.obtener_conexion()

        try:

            # Precio por habitacion
            dao_habitacion = HabitacionDAO(conexion)
            precio_por_noche = dao_habitacion.obtener_precio_por_habitacion(id_habitacion)
            reserva.total = noches_totales * precio_por_noche

            # Registro de clientes
            dao_cliente = ClienteDAO(conexion)
            id_generado_cliente = dao_cliente.insertar_cliente(cliente)

            # Registro de reserva
            reserva.id_cliente = id_generado_cliente
            dao_reserva = ReservaDAO(conexion)
            id_generado_reseva = dao_reserva.insertar_reserva(reserva)

            # Registro de habitacion   
            reserva_habitacion = ReservaHabitacion(id_habitacion, id_generado_reseva)
            dao_reserva_habitacion = ReservaHabitacionDAO(conexion)
            dao_reserva_habitacion.insertar_reserva_habitacion(reserva_habitacion)

            # Registro de acompañantes
            dao_acompanante = AcompananteDAO(conexion)
            for acompanante in acompanantes:
                acompanante.id_reserva = id_generado_reseva
                dao_acompanante.insertar_acompanante(acompanante)

            conexion.commit()

            return id_generado_reseva
        
        except Exception as e:
            conexion.rollback()
            raise Exception(f"Ha ocurrido un error en la Base de Datos: {e}")
            

