from config.database import ConexionDB
from models import Usuario

from daos.usuario_dao import UsuarioDAO

class AuthController:
    def __init__(self):
        self.db = ConexionDB()

    def registrar_nuevo_usuario(self, usuario: "Usuario") -> None:
        
        conexion = self.db.obtener_conexion()

        try:

            dao_usuario = UsuarioDAO(conexion)

            return dao_usuario.insertar_nuevo_usuario(usuario)

        except Exception as e:
            raise Exception(f"Ha ocurrido un error en la Base de Datos: {e}")
        finally:
            self.db.cerrar_conexion()