from config.database import ConexionDB
from models.cliente import Cliente

class ClienteDAO:
    def __init__(self):
        self.db = ConexionDB()
        self.conexion = self.db.obtener_conexion()

    def insertar_cliente(self, cliente: "Cliente"):

        cursor = self.conexion.cursor()

        try:

            sql = """
                INSERT INTO cliente (nombre, apellido, dni, telefono, correo, direccion)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING idcliente;
            """

            valores = (
                cliente.nombre,
                cliente.apellido,
                cliente.dni,
                cliente.telefono,
                cliente.correo,
                cliente.direccion
            )

            cursor.execute(sql, valores)
            id_generado = cursor.fetchone()[0]
            self.conexion.commit()

            return id_generado

        except Exception as e:
            self.conexion.rollback()
            raise e
        finally:
            if cursor:
                cursor.close()
