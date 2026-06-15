from typing import List, Tuple, Any

class BaseDAO:
    def __init__(self, conexion):
        self.conexion = conexion

    def insertar_datos(self, sql: str, valores: Tuple[Any][Any]) -> int:
        cursor = self.conexion.cursor()
        try:
            cursor.execute(sql, valores)
            self.conexion.commit()
            id_obtenido = cursor.fetchone()[0]

            return id_obtenido
        except Exception as e:
            self.conexion.rollback()
            raise Exception(f"Error al insertar en la Base de Datos: {e}")
        finally:
            if cursor:
                cursor.close()

    def obtener_un_registro(self, sql: str, valores: Tuple[Any] = None) -> List:
        cursor = self.conexion.cursor()
        try:
            if valores:
                cursor.execute(sql, valores)
            else:
                cursor.execute(sql)
            return cursor.fetchone()
        except Exception as e:
            raise Exception(f"Error al obtener registro: {e}")
        finally:
            if cursor:
                cursor.close()

    def obtener_varios_datos(self, sql: str, valores: Tuple[Any] = None) -> List:
        cursor = self.conexion.cursor()
        try:
            if valores:
                cursor.execute(sql, valores)
            else:
                cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            raise Exception(f"Error al obtener datos: {e}")
        finally:
            if cursor:
                cursor.close()
    
    def obtener_un_dato_por_id(self, sql: str, id_obtenido: int) -> Tuple[Any]:
        return self.obtener_un_registro(sql, (id_obtenido,))
                
    def obtener_varios_datos_por_id(self, sql: str, id_obtenido: int) -> List:

        return self.obtener_varios_datos(sql, (id_obtenido,))

    def actualizar_datos(self, sql: str, valores: Tuple[Any]) -> None:
        cursor = self.conexion.cursor()
        try:

            cursor.execute(sql, valores)
            self.conexion.commit()

            if cursor.rowcount == 0:
                raise Exception("No se encontró el registro para actualizar")
        except Exception as e:
            self.conexion.rollback()
            raise Exception(f"Error al actualizar: {e}")
        finally:
            if cursor:
                cursor.close()

    def eliminar_dato_por_id(self, sql: str, id_param: int) -> None:
        cursor = self.conexion.cursor()
        try:

            cursor.execute(sql, (id_param,))
            self.conexion.commit()

            if cursor.rowcount == 0:
                raise Exception("No se encontro el registro para eliminar")
            
        except Exception as e:
            self.conexion.rollback()
            raise Exception(f"Error al eliminar: {e}")
        finally:
            if cursor:
                cursor.close()

    def cambiar_estado(self, sql: str, valores: Tuple[Any]) -> bool:
        cursor = self.conexion.cursor()
        try:
            cursor.execute(sql, valores)
            self.conexion.commit()
            
            if cursor.rowcount == 0:
                raise Exception("No se pudo completar el cambio de estado")
                
            return True
        except Exception as e:
            self.conexion.rollback()
            raise Exception(f"Error al cambiar estado: {e}")
        finally:
            if cursor:
                cursor.close()