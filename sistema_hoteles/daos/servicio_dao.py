from config.database import ConexionDB
from models.servicio import Servicio

class ServicioDAO:
    def __init__(self):
        self.db = ConexionDB()
        self.conexion = self.db.obtener_conexion()

    def insertar_servicio(self, servicio: "Servicio") -> int:

        cursor = self.conexion.cursor()

        try:
            
            consulta = """
                INSERT INTO servicio (nombre, descripcion, precio) 
                VALUES (%s, %s, %s)
                RETURNING idservicio
            """

            valores = (
                servicio.nombre,
                servicio.descripcion,
                servicio.precio
            )

            cursor.execute(consulta, valores)
            id_obtenido = cursor.fetchone()[0]
            self.conexion.commit()

            return id_obtenido

        except Exception as e:
            return e
        finally:
            if cursor:
                cursor.close()