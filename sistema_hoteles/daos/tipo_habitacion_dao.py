from config.database import ConexionDB
from models.tipo_habitacion import TipoHabitacion


class TipoHabitacionDAO:
    def __init__(self):
        self.db = ConexionDB()
        self.conexion = self.db.obtener_conexion()

    def insertar_tipo_habitacion(self, tipo_habitacion: "TipoHabitacion") -> int:

        cursor = self.conexion.cursor()

        try:

            consulta = """
                INSERT INTO tipo_habitacion (nombre, precio, capacidad)
                VALUES (%s, %s, %s)
                RETURNING idtipo_habitacion
            """

            valores = (
                tipo_habitacion.nombre,
                tipo_habitacion.precio,
                tipo_habitacion.capacidad
            )

            cursor.execute(consulta, valores)
            id_obtenido = cursor.fetchone()[0]
            self.conexion.commit()

        except Exception as e:
            self.conexion.rollback()
            raise e
        finally:
            if cursor:
                cursor.close()