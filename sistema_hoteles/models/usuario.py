from pydantic import BaseModel

class UsuarioSchema(BaseModel):
    nombre: str
    apellido: str
    contrasena: str
    rol: str

class Usuario:
    def __init__(self, nombre: str, apellido: str, contrasena: str, rol: str, id_usuario: None = None):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.apellido = apellido
        self.contrasena = contrasena
        self.rol = rol
