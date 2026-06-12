from config.database import ConexionDB
from pydantic import ValidationError

from models import Usuario, UsuarioSchema
from daos.usuario_dao import UsuarioDAO

class AuthController:
    def __init__(self):
        self.db = ConexionDB()

    def registrar_nuevo_usuario(self, nombre: str, contrasena: str, rol: str) -> None:
        
        try:
            validador_usuario = UsuarioSchema(
                nombre=nombre,
                contrasena=contrasena,
                rol=rol
            )   
        except ValidationError as e:
            raise ValueError("Por favor, revisa que los datos ingreados sean correctos")
        
        usuario = Usuario(
            nombre=validador_usuario.nombre,
            contrasena=validador_usuario.contrasena,
            rol=validador_usuario.rol
        )

        conexion = self.db.obtener_conexion()
        try:

            dao_usuario = UsuarioDAO(conexion)
            return dao_usuario.insertar_nuevo_usuario(usuario)
        
            

        except Exception as e:
            raise Exception(f"Ha ocurrido un error en la Base de Datos: {e}")