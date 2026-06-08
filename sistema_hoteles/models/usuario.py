from pydantic import BaseModel

class UsuarioSchema(BaseModel):
    nombre: str
    apellido: str
    contrasena: str
    rol: str

class Usuario:
    def __init__(self, id_usuario: None, nombre: str, apellido: str, contrasena: str, rol: str):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.apellido = apellido
        self.contrasena = contrasena
        self.rol = rol
