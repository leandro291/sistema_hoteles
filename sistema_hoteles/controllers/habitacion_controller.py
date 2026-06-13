from config.database import ConexionDB

from pydantic import ValidationError
from decimal import Decimal

from tkinter import messagebox
from models.tipo_habitacion import TipoHabitacion, TipoHabitacionSchema
from daos.tipo_habitacion_dao import TipoHabitacionDAO

class HabitacionController:
    def __init__(self):
        self.db =  ConexionDB()

    def registrar_tipo_de_habitacion(self, nombre: str, precio: float, capacidad: int, descripcion: str ) -> None:

        precio_limpio = Decimal(str(precio))
        print(precio_limpio)

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

