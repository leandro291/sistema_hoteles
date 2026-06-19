from typing import Tuple, Any
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
    
    def obtener_todos_los_clientes(self) -> Tuple[Any]:

        consulta = """
            SELECT 
                id_cliente,
                nombre,
                apellido,
                tipo_documento,
                num_documento,
                telefono,
                correo,
                direccion
            FROM cliente
        """

        return self.obtener_varios_datos(consulta)
    
    def contar_total_clientes(self) -> int:

        consulta = """
            SELECT  
            COUNT(*) 
            FROM cliente 
        """

        res = self.obtener_un_registro(consulta)
        return res[0]
    
    def actualizar_datos_cliente(self, cliente: "Cliente") -> None:

        consulta = """
            UPDATE cliente
            SET 
                nombre = %s, 
                apellido = %s, 
                tipo_documento = %s, 
                num_documento = %s, 
                telefono = %s, 
                correo = %s, 
                direccion = %s
            WHERE id_cliente = %s;
        """

        valores = (
            cliente.nombre,
            cliente.apellido,
            cliente.tipo_documento,
            cliente.numero_documento,
            cliente.telefono,
            cliente.correo,
            cliente.direccion,
            cliente.id_cliente
        )

        self.actualizar_datos(consulta, valores)
    
    def eliminar_cliente(self, id_cliente: int) -> None:
        
        consulta = "DELETE FROM cliente WHERE id_cliente = %s;"
        
        self.eliminar_dato_por_id(consulta, id_cliente)
    
    



