from config.database import ConexionDB

class BaseDAO:
    def __init__(self, conexion : "ConexionDB"):
        self.conexion = conexion

    def insertar_y_retornar_id(self, sql: str, valores: tuple) -> int:

        cursor = self.conexion.cursor()

        try:

            cursor.execute(sql, valores)
            id_obtenido = cursor.fetchone()[0]
            return id_obtenido

        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()

    def insertar_sin_retorno_id(self, sql, valores: tuple):

        cursor = self.conexion.cursor()

        try:

            cursor.execute(sql, valores)
            return True

        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()