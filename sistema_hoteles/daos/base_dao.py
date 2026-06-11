from config.database import ConexionDB

class BaseDAO:
    def __init__(self, conexion):
        self.conexion = conexion

    def insertar_datos(self, sql: str, valores: tuple) -> int:

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
    
    def obtener_dato_por_id(self, sql: str, id: int) -> int:
        pass

    def actualizar_dato_por_id(self, sql: str, id: int) -> None:
        pass

    def eliminar_dato_por_id(self, sql: str, id: int) -> None:
        
        cursor = self.conexion.cursor()

        try:

            cursor.execute(sql, id)
            res = cursor.fetchone()

            return res
        
        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()

    def cambiar_estado(self, sql: str, valores: tuple) -> bool:

        cursor = self.conexion.cursor()

        try:

            cursor.execute(sql, valores)
            if cursor.rowcount == 0:
                raise Exception(f"La reserva ingresada no existe")
                
            return True

        except Exception as e:
            raise e
        finally:
            if cursor:
                cursor.close()