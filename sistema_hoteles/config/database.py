import psycopg2

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
                dbname='hotelesdb',
                user='postgres',
                password='root',
                host='localhost',
                port='5432'
            )
        except Exception as e:
            raise ValueError(f"Ha ocurrido un error:  {e}")

    def obtener_conexion(self):
        return self._conexion
    
    def cerrar_conexion(self):
        if self._conexion:
            self._conexion.close()

if __name__ == "__main__":
    db = ConexionDB()

    print(db.obtener_conexion())