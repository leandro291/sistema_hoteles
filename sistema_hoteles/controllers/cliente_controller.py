from config.database import ConexionDB

from pydantic import ValidationError

from models.cliente import Cliente, ClienteSchema
from daos.cliente_dao import ClienteDAO

class ClienteController:
    def __init__(self):
        self.db = ConexionDB()

    def registrar_usuario(self, nombre: str, apellido: str, tipo_doc: str, num_doc: str, telefono: str, 
                        correo: str, direccion: str) -> None:
        
        try:
            validador_cliente = ClienteSchema(
                nombre=nombre,
                apellido=apellido,
                tipo_documento=tipo_doc,
                numero_documento=num_doc,
                telefono=telefono,
                correo=correo,
                direccion=direccion
            )
        except ValidationError as e:
            raise ValueError(f"Ha ocurrido un error al ingresar los datos: {e}")
        
        cliente = Cliente(
            nombre=validador_cliente.nombre,
            apellido=validador_cliente.apellido,
            tipo_documento=validador_cliente.tipo_documento,
            numero_documento=validador_cliente.numero_documento,
            telefono=validador_cliente.telefono,
            correo=validador_cliente.correo,
            direccion=validador_cliente.direccion
        )

        conexion = self.db.obtener_conexion()

        try:

            dao_cliente = ClienteDAO(conexion)
            return dao_cliente.insertar_cliente(cliente)

        except Exception as e:
            raise Exception(f"Ha ocurrido un error al insertar clientes: {e}")
        
    def obtener_todos_clientes(self):
        
        conexion = self.db.obtener_conexion()

        try:
            dao_cliente = ClienteDAO(conexion)
            return dao_cliente.obtener_todos_los_clientes()
        except Exception as e:
            raise Exception(f"Ha ocurrido un error al obtener los datos del cliente: {e}")
        
    def actualizar_cliente(self, id_cliente: int, nombre: str, apellido: str, tipo_doc: str, num_doc: str,
                        telefono: str, correo: str, direccion: str):
        
        conexion = self.db.obtener_conexion()

        try:
            validador_cliente = ClienteSchema(
                nombre=nombre,
                apellido=apellido,
                tipo_documento=tipo_doc,
                numero_documento=num_doc,
                telefono=telefono,
                correo=correo,
                direccion=direccion
            )
        except ValidationError as e:
            raise ValueError(f"Ha ocurrido un error en los valores del cliente: {e}")
        
        cliente_actualizado = Cliente(
            nombre=validador_cliente.nombre,
            apellido=validador_cliente.apellido,
            tipo_documento=validador_cliente.tipo_documento,
            numero_documento=validador_cliente.numero_documento,
            telefono=validador_cliente.telefono,
            correo=validador_cliente.correo,
            direccion=validador_cliente.direccion,
            id_cliente=id_cliente
        )

        try:

            dao_cliente = ClienteDAO(conexion)
            dao_cliente.actualizar_datos_cliente(cliente_actualizado)

        except Exception as e:
            raise Exception(f"Ha ocurrido un error al actualizar un cliente: {e}")
        
    def eliminar_cliente(self, id_cliente: int) -> None:

        conexion = self.db.obtener_conexion()

        try:

            dao_cliente = ClienteDAO(conexion)
            dao_cliente.eliminar_cliente(id_cliente)

        except Exception as e:
            raise Exception(f"Ha ocurrido un error al eliminar un cliente: {e}")
        
    def contar_total_clientes(self):

        conexion = self.db.obtener_conexion()

        try:

            dao_cliente = ClienteDAO(conexion)
            return dao_cliente.contar_totaL_clientes()

        except Exception as e:
            raise Exception(f"Ha ocurrido un error al eliminar un cliente: {e}")