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
from typing import List, Dict, Any

class RecepcionController:
    def __init__(self):
        self.db = ConexionDB()

    def registrar_check_in(self, cliente: "Cliente", reserva: "Reserva", id_usuario: int, selecciones: List[Dict[str, Any]]):

        # Logica para obtener las fechas para la reserva
        try:
            fecha_entrada = datetime.strptime(reserva.fecha_entrada, "%Y-%m-%d")
            fecha_salida = datetime.strptime(reserva.fecha_salida, "%Y-%m-%d")
            noches_totales = (fecha_salida - fecha_entrada).days

            if noches_totales <= 0:
                raise ValueError("La fecha de salida debe ser mayor a la de entrada")
            
        except Exception as e:
            raise ValueError(f"Ha ocurrio un error a la hora de validar las fechas: {e}")
        
        conexion = self.db.obtener_conexion()

        try:

            #Datos del cliente
            dao_cliente = ClienteDAO(conexion)
            id_obtenido_cliente = dao_cliente.insertar_cliente(cliente)

            #Datos de la reserva
            reserva.id_usuario = id_usuario
            reserva.estado_reserva = "En curso"
            reserva.id_cliente = id_obtenido_cliente

            dao_reserva = ReservaDAO(conexion)
            id_obtenido_reserva = dao_reserva.insertar_reserva(reserva)

            #Datos de la reserva en la habitacion
            dao_habitacion = HabitacionDAO(conexion)
            dao_reserva_habitacion = ReservaHabitacionDAO(conexion)
            dao_acompanante = AcompananteDAO(conexion)

            for seleccion in selecciones:
                id_hab_actual = seleccion["id_habitacion"]
                tiene_titular = seleccion["tiene_titular"]
                acompanantes_actuales = seleccion.get("acompanantes", [])

                capacidad_maxima = dao_habitacion.obtener_cantidad_por_habitacion(id_hab_actual)                
                cantidad_titular = 1 if tiene_titular else 0
                total_personas = cantidad_titular + len(acompanantes_actuales)

                if total_personas == 0:
                    raise ValueError(f"La habitación {id_hab_actual} no tiene ocupantes asignados.")
                
                if total_personas > capacidad_maxima:
                    raise ValueError(f"Capacidad excedida en la habitación {id_hab_actual}. Soporta {capacidad_maxima}, intentan registrar {total_personas}.")

                precio_por_noche = dao_habitacion.obtener_precio_por_habitacion(id_hab_actual)
                subtotal = precio_por_noche * noches_totales

                nueva_reserva_habitacion = ReservaHabitacion(
                    id_habitacion=id_hab_actual,
                    id_reserva=id_obtenido_reserva,
                    precio_por_noche=precio_por_noche,
                    es_titular=tiene_titular,
                    subtotal=subtotal,
                    id_reserva_habitacion=None
                )

                id_generado_reserva_habitacion = dao_reserva_habitacion.insertar_reserva_habitacion(nueva_reserva_habitacion)

                # Insertar los acompañantes en su respectiva habitación
                for acompanante in acompanantes_actuales:
                    acompanante.id_reserva_habitacion = id_generado_reserva_habitacion
                    dao_acompanante.insertar_acompanante(acompanante)
            
            conexion.commit()
        
        except Exception as e:
            conexion.rollback()
            raise Exception(f"Ha ocurrido un error en la Base de Datos: {e}")
        finally:
            if conexion:
                conexion.close()
            

