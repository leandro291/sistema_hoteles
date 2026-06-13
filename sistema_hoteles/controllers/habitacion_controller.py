from config.database import ConexionDB

from pydantic import ValidationError
from decimal import Decimal

from tkinter import messagebox
from models.habitacion import Habitacion, HabitacionSchema
from models.tipo_habitacion import TipoHabitacion, TipoHabitacionSchema
from daos.tipo_habitacion_dao import TipoHabitacionDAO
from daos.habitacion_dao import HabitacionDAO

class HabitacionController:
    def __init__(self):
        self.db =  ConexionDB()

    def registrar_tipo_de_habitacion(self, nombre: str, precio: float, capacidad: int, descripcion: str ) -> None:

        precio_limpio = Decimal(str(precio))

        try:
            validador_tipo = TipoHabitacionSchema(
                nombre=nombre,
                precio=precio_limpio,
                capacidad=capacidad,
                descripcion=descripcion
            )
        except ValidationError as e:
            raise ValueError(f"Por favor revise los datos ingresados {e}")
        
        tipo = TipoHabitacion(
            nombre=validador_tipo.nombre,
            precio = validador_tipo.precio,
            capacidad = validador_tipo.capacidad,
            descripcion = validador_tipo.descripcion
        )

        conexion = self.db.obtener_conexion()

        try:

            dao_tipo = TipoHabitacionDAO(conexion)
            return dao_tipo.insertar_tipo_habitacion(tipo)
        except ValueError as e:
            messagebox.showerror("Datos invalidados", str(e))
        except Exception as e:
            raise Exception(f"Ha ocurrido un error en la base de datos: {e}")
        
    def registrar_habitacion(self, num_piso: int, num_habitacion: str, id_tipo_habitacion: int ) -> None:
        
        try:
            validador_habitacion = HabitacionSchema(
                numero_piso=num_piso,
                numero_habitacion=num_habitacion
            )
        except ValidationError as e:
            raise ValueError("Ha ocurrido un error al ingresar los datos")
        
        habitacion = Habitacion(
            numero_piso=validador_habitacion.numero_piso,
            numero_habitacion=validador_habitacion.numero_habitacion,
            estado="Disponible",
            id_tipo_habitacion=id_tipo_habitacion
        )

        conexion = self.db.obtener_conexion()

        try:

            dao_habitacion = HabitacionDAO(conexion)
            return dao_habitacion.insertar_habitacion(habitacion)

        except Exception as e:
            raise Exception(f"Ha ocurrido un error en la base de datos: {e}")
        
    def obtener_detalle_habitacion(self, id_habitacion):

        conexion = self.db.obtener_conexion()
            
        try:
            dao_habitacion = HabitacionDAO(conexion)
            datos_completos = dao_habitacion.obtener_detalles_por_habitacion(id_habitacion)
            return datos_completos
            
        except Exception as e:
            raise Exception(f"Ha ocurrido un error en la base de datos: {e}")
        
    def obtener_todas_las_habitaciones(self):
        conexion = self.db.obtener_conexion()
        try:
            dao_habitacion = HabitacionDAO(conexion)
            resultados = dao_habitacion.obtener_todas_las_habitaciones()
            return resultados
        except Exception as e:
            raise Exception(f"Ha ocurrido un error en la base de datos: {e}")
            

    def obtener_tipos_de_habitacion(self):
        conexion = self.db.obtener_conexion()
        try:

            dao_tipo = TipoHabitacionDAO(conexion)
            return dao_tipo.obtener_todos_los_tipos()

        except Exception as e:
            raise Exception(f"Ha ocurrido un error en la base de datos: {e}")