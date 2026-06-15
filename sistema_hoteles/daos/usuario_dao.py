from daos import BaseDAO
from typing import Tuple, Any
from models.usuario import Usuario


class UsuarioDAO(BaseDAO):
    
    def insertar_nuevo_usuario(self, usuario: "Usuario") -> int:

        consulta = """
            INSERT INTO usuario (nombre_usuario, contrasena, rol)
            VALUES (%s, %s, %s)
            RETURNING id_usuario
        """

        valores = (
            usuario.nombre,
            usuario.contrasena,
            usuario.rol
        )

        return self.insertar_datos(consulta, valores)
    
    def obtener_usuario_por_nombre(self, nombre_usuario: str) -> Tuple[Any]:

        consulta = """
            SELECT id_usuario, contrasena, rol
            FROM usuario
            WHERE nombre_usuario = %s
        """

        valores = (nombre_usuario, )

        return self.obtener_un_registro(consulta, valores)