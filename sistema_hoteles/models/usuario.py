from pydantic import BaseModel


class UsuarioSchema(BaseModel):
    nombre: str
    contrasena: str
    rol: str


class Usuario:
    def __init__(self, nombre: str, contrasena: str, rol: str, id_usuario: int | None = None):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.contrasena = contrasena
        self.rol = rol

    def __str__(self):
        return f"Usuario(id={self.id_usuario}, nombre='{self.nombre}', rol='{self.rol}')"
