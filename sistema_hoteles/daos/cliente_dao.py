from daos.base_dao import BaseDAO
from models.cliente import Cliente

class ClienteDAO(BaseDAO):

    def insertar_cliente(self, cliente: "Cliente") -> int:

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

        return self.insertar_y_retornar_id(sql, valores)




