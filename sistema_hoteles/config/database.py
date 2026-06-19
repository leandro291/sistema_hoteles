import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

class ConexionDB:

    _instancia = None

    def __new__(cls, *args):

        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        
        return cls._instancia
    
    def __init__(self):
        if not hasattr(self, 'inicializado'):
            self._conexion = None
            self._conectar()
            self.inicializado = True
    
    def _conectar(self):
        try:
            self._conexion = psycopg2.connect(
                dbname=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT')
            )
        except Exception as e:
            raise ConnectionError(f"Error al conectar a la base de datos: {e}")

    def obtener_conexion(self):
        if self._conexion is None or self._conexion.closed:
            self._conectar()
        return self._conexion
    
    def cerrar_conexion(self):
        if self._conexion:
            self._conexion.close()
            self._conexion = None

if __name__ == "__main__":
    db = ConexionDB()