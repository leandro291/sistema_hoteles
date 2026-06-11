from daos.base_dao import BaseDAO
from models.cliente import Cliente

class ClienteDAO(BaseDAO):

    def insertar_cliente(self, cliente: "Cliente") -> int:

        sql = """
            INSERT INTO cliente (nombre, apellido, tipo_documento, num_documento, telefono, correo, direccion)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id_cliente;
        """

        valores = (
            cliente.nombre,
            cliente.apellido,
            cliente.tipo_documento,
            cliente.numero_documento,
            cliente.telefono,
            cliente.correo,
            cliente.direccion,
        )

        return self.insertar_datos(sql, valores)




