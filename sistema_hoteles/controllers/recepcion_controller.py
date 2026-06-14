from config.database import ConexionDB

from pydantic import ValidationError

from models.reserva import Reserva, ReservaSchema
from models.acompanante import Acompanante, AcompananteSchema
from models.reserva_habitacion import ReservaHabitacion

from daos.reserva_dao import ReservaDAO
from daos.habitacion_dao import HabitacionDAO
from daos.reserva_habitacion_dao import ReservaHabitacionDAO
from daos.acompanante_dao import AcompananteDAO

from datetime import datetime
from typing import List, Dict, Any

class RecepcionController:
    def __init__(self):
        self.db = ConexionDB()

    def registrar_check_in(self, id_cliente: int, datos_reserva: dict, id_usuario: int, selecciones: list):
        
        try:
            fecha_entrada = datetime.strptime(datos_reserva["fecha_entrada"], "%Y-%m-%d")
            fecha_salida = datetime.strptime(datos_reserva["fecha_salida"], "%Y-%m-%d")
            noches_totales = (fecha_salida - fecha_entrada).days

            if noches_totales <= 0:
                raise ValueError("La fecha de salida debe ser estrictamente posterior a la fecha de entrada")
                
        except ValueError as e:
            raise ValueError(f"Error en validación de fechas: {e}")

        try:
            validador_reserva = ReservaSchema(
                fecha_entrada=fecha_entrada,
                fecha_salida=fecha_salida
            )
        except ValidationError as e:
            raise ValueError("Ha ocurrido un error al ingresar los datos de las fechas")
        
        reserva = Reserva(
            id_cliente=id_cliente,
            id_usuario=id_usuario,
            fecha_entrada=validador_reserva.fecha_entrada,
            fecha_salida=validador_reserva.fecha_salida,
            estado_reserva="En curso"
        )

        conexion = self.db.obtener_conexion()

        try:
            dao_reserva = ReservaDAO(conexion)
            id_obtenido_reserva = dao_reserva.insertar_reserva(reserva)
        except Exception as e:
            raise Exception(f"1Ha ocurrido un error en la base de datos: {e}")

        try:
            
            for seleccion in selecciones:

                id_habitacion_actual = seleccion["id_habitacion"]
                tiene_titular = seleccion["tiene_titular"]
                acompanantes_crudos = seleccion.get("acompanantes", [])

                dao_habitacion = HabitacionDAO(conexion)
        
                capacidad_maxima = dao_habitacion.obtener_cantidad_por_habitacion(id_habitacion_actual)                
                cantidad_titular = 1 if tiene_titular else 0
                total_personas = cantidad_titular + len(acompanantes_crudos)

                if total_personas == 0:
                        raise ValueError(f"La habitación seleccionada no tiene ocupantes asignados.")
                    
                if total_personas > capacidad_maxima:
                        raise ValueError(f"Intento de vulneración de capacidad: Se intentó registrar {total_personas} personas en un cuarto de capacidad {capacidad_maxima}.")


                precio_por_noche = dao_habitacion.obtener_precio_por_habitacion(id_habitacion_actual)
                if precio_por_noche is None or precio_por_noche <= 0:
                    raise ValueError("Error al obtener la tarifa de la habitación desde la base de datos.")
                    
                subtotal_calculado = precio_por_noche * noches_totales

                dao_reserva_habitacion = ReservaHabitacionDAO(conexion)

                reserva_habitacion = ReservaHabitacion(
                    id_habitacion=id_habitacion_actual,
                    id_reserva=id_obtenido_reserva,
                    precio_por_noche=precio_por_noche,
                    es_titular=tiene_titular,
                    subtotal=subtotal_calculado,
                )
                id_generado_reserva_habitacion = dao_reserva_habitacion.insertar_reserva_habitacion(reserva_habitacion)

                dao_habitacion.cambiar_estado_habitacion(id_habitacion_actual, "Ocupado")

                dao_acompanante = AcompananteDAO(conexion)

                for diccionario_acompanantes in acompanantes_crudos:

                    try:
                        validador_acompanante = AcompananteSchema(
                            nombre=diccionario_acompanantes["nombre"],
                            apellido=diccionario_acompanantes["apellido"],
                            tipo_documento=diccionario_acompanantes["tipo_documento"],
                            numero_documento=diccionario_acompanantes["num_documento"],
                            telefono=diccionario_acompanantes["telefono"],
                        )
                    except ValidationError as e:
                        raise ValueError("Ha ocurrido un error al ingresar los datos")

                    acompanante = Acompanante(
                        nombre=validador_acompanante.nombre,
                        apellido=validador_acompanante.apellido,
                        tipo_documento=validador_acompanante.tipo_documento,
                        numero_documento=validador_acompanante.numero_documento,
                        telefono=validador_acompanante.telefono,
                        id_reserva_habitacion=id_generado_reserva_habitacion
                    )

                    dao_acompanante.insertar_acompanante(acompanante)

        except Exception as e:
            raise Exception(f"2Ha ocurrido un error en la base de datos: {e}")
                

