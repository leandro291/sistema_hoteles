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
            raise ValueError(f"Ha ocurrido un error al ingresar los datos")
        
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
            raise Exception(f"Ha ocurrido un error en la base de datos: {e}")