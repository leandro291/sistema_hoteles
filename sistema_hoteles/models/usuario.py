from pydantic import BaseModel

class UsuarioSchema(BaseModel):
    nombre: str
    contrasena: str
    rol: str

class Usuario:
    def __init__(self, nombre: str, contrasena: str, rol: str, id_usuario: None = None):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.contrasena = contrasena
        self.rol = rol
