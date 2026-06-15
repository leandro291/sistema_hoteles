from pydantic import ValidationError
from config.database import ConexionDB
from typing import Dict

from daos.usuario_dao import UsuarioDAO
from models import Usuario, UsuarioSchema

from utils.security import hashear_contrasena, validar_contrasena

class AuthController:
    def __init__(self):
        self.db = ConexionDB()

    def registrar_nuevo_usuario(self, nombre: str, contrasena: str, rol: str) -> int:
        
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
            contrasena=hashear_contrasena(validador_usuario.contrasena),
            rol=validador_usuario.rol
        )

        conexion = self.db.obtener_conexion()

        try:
            dao_usuario = UsuarioDAO(conexion)
            return dao_usuario.insertar_nuevo_usuario(usuario)
        except Exception as e:
            raise Exception(f"Ha ocurrido un error en la Base de Datos: {e}")
        
    def iniciar_sesion(self, nombre_ingresado: str, contrasena_ingresada: str) -> Dict[str]:
        
        conexion = self.db.obtener_conexion()

        try:
            dao_usuario = UsuarioDAO(conexion)
            datos = dao_usuario.obtener_usuario_por_nombre(nombre_ingresado)

            if not datos:
                raise ValueError("El nombre o la contraseña es erroneo")
            
            id_usuario, contrasena, rol = datos

            if not validar_contrasena(contrasena_ingresada, contrasena):
                raise ValueError("El nombre o la contraseña es erroneo")
            
            return {
                "id_usuario": id_usuario,
                "nombre_usuario": nombre_ingresado,
                "rol" : rol
            }
        
        except Exception as e:
            raise Exception(f"Ha ocurrido un error en la Base de Datos: {e}")