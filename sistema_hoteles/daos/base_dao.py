class BaseDAO:
    def __init__(self, conexion):
        self.conexion = conexion

    def insertar_datos(self, sql: str, valores: tuple) -> int:

        cursor = self.conexion.cursor()

        try:

            cursor.execute(sql, valores)

            self.conexion.commit()
            id_obtenido = cursor.fetchone()[0]
            return id_obtenido
        
        except Exception as e:
            self.conexion.rollback()
            raise Exception(f"Ha ocurrido un error en la Base de Datos: {e}")
        finally:
            if cursor:
                cursor.close()

    def obtener_un_registro(self, sql: str, valores: tuple):

        cursor = self.conexion.cursor()

        try:

            cursor.execute(sql, valores)

            self.conexion.commit()
            datos = cursor.fetchone()
            return datos
        
        except Exception as e:
            self.conexion.rollback()
            raise Exception(f"Ha ocurrido un error en la Base de Datos: {e}")
        finally:
            if cursor:
                cursor.close()
    
    def obtener_dato_por_id(self, sql: str, id: int) -> int:

        cursor = self.conexion.cursor()

        try:

            cursor.execute(sql, id)
            self.conexion.commit()

            res = cursor.fetchone()

            return res
        
        except Exception as e:
            self.conexion.rollback()
            raise Exception(f"Ha ocurrido un error en la Base de Datos: {e}")
        finally:
            if cursor:
                cursor.close()

    def actualizar_dato_por_id(self, sql: str, id: int) -> None:
        pass

    def eliminar_dato_por_id(self, sql: str, id: int) -> None:
        cursor = self.conexion.cursor()
        try:

            cursor.execute(sql, id)
            self.conexion.commit()

            if cursor.rowcount == 0:
                raise Exception("No se encontró el registro para eliminar")

        except Exception as e:
            self.conexion.rollback()
            raise Exception(f"Ha ocurrido un error en la Base de Datos: {e}")
        finally:
            cursor.close()

    def cambiar_estado(self, sql: str, valores: tuple) -> bool:

        cursor = self.conexion.cursor()

        try:

            cursor.execute(sql, valores)
            self.conexion.commit()
            
            if cursor.rowcount == 0:
                raise Exception(f"La reserva ingresada no existe")
                
            return True

        except Exception as e:
            self.conexion.rollback()
            raise Exception(f"Ha ocurrido un error en la Base de Datos: {e}")
        finally:
            if cursor:
                cursor.close()