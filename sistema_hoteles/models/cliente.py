from pydantic import BaseModel, field_validator, Field, EmailStr

class ClienteSchema(BaseModel):
    nombre: str
    apellido: str
    tipo_documento: str
    numero_documento: str
    telefono: str
    correo: EmailStr
    direccion: str

    @field_validator('telefono')
    @classmethod
    def validate_telefono(cls, valor: str) -> str:

        if len(valor) != 9 or not valor.isdigit():
            raise ValueError("El teléfono debe tener exactamente 9 digitos")
        
        return valor
    
    @field_validator('numero_documento')
    def validate_numero_documento(cls, valor: str) -> str:
        if not valor.isdigit():
            raise ValueError(f"El Numero de Documento {valor} debe estar formado de digitos")
        
        return valor
    
    @field_validator('nombre', 'apellido')
    @classmethod
    def validate_no_numeros(cls, valor: str) -> str:
        if any(char.isdigit() for char in valor):
            raise ValueError("El nombre y el apellido no deben contener numeros")
            
        return valor

class Cliente:
    def __init__(self, nombre: str, apellido: str, tipo_documento: str, numero_documento: str, 
                 telefono: str, correo: str, direccion: str, id_cliente: None = None):
        
        self.id_cliente = id_cliente
        self.nombre = nombre
        self.apellido = apellido
        self.tipo_documento = tipo_documento
        self.numero_documento = numero_documento
        self.telefono = telefono
        self.correo = correo
        self.direccion = direccion
