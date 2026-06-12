from daos import BaseDAO
from models.usuario import Usuario


class UsuarioDAO(BaseDAO):
    
    def insertar_nuevo_usuario(self, usuario: "Usuario") -> None:

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