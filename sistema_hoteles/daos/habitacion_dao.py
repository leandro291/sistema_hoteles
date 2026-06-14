from daos.base_dao import BaseDAO
from models.habitacion import Habitacion

class HabitacionDAO(BaseDAO):
    
    def insertar_habitacion(self, habitacion: "Habitacion") -> int:

        consulta = """
            INSERT INTO habitacion (num_piso, num_habitacion, estado, id_tipo_habitacion)
            VALUES (%s, %s, %s, %s)
            RETURNING id_habitacion
        """

        valores = (
            habitacion.numero_piso,
            habitacion.numero_habitacion,
            habitacion.estado,
            habitacion.id_tipo_habitacion
        )

        return self.insertar_datos(consulta, valores)
    
    def obtener_detalles_por_habitacion(self, id_habitacion: int):
        
        consulta = """

            SELECT 
                h.num_habitacion,
                t.nombre,
                t.capacidad,
                t.precio,
                h.estado,
                h.num_piso
            FROM habitacion h
            JOIN tipo_habitacion t ON h.id_tipo_habitacion = t.id_tipo_habitacion
            WHERE h.id_habitacion = %s

        """

        return self.obtener_dato_por_id(consulta, id_habitacion)
    
    def obtener_todas_las_habitaciones(self):

        consulta = """
            SELECT id_habitacion, num_habitacion FROM habitacion;
        """

        return self.obtener_datos(consulta)
    
    def obtener_habitaciones_disponibles(self):

        consulta = """
            SELECT 
                h.id_habitacion, 
                h.num_habitacion, 
                th.capacidad 
            FROM habitacion h
            JOIN tipo_habitacion th ON h.id_tipo_habitacion = th.id_tipo_habitacion
            WHERE h.estado = 'Disponible';
        """

        return self.obtener_datos(consulta)

    def cambiar_estado_habitacion(self, id_habitacion: int, nuevo_estado: str) -> bool:
        
        consulta = """
            UPDATE 
            habitacion 
            SET estado = %s 
            WHERE id_habitacion = %s
        """

        valores = (nuevo_estado, id_habitacion)

        self.cambiar_estado(consulta, valores)
        
    def obtener_precio_por_habitacion(self, id_habitacion: int) -> float:

        consulta = """
            SELECT th.precio
            FROM habitacion h
            JOIN tipo_habitacion th ON h.id_tipo_habitacion = th.id_tipo_habitacion
            WHERE h.id_habitacion = %s
        """

        valores = (id_habitacion, )

        resultado = self.obtener_dato_por_id(consulta, valores)
        
        if resultado:
            return float(resultado[0]) 
        return 0.0 
    
    def obtener_cantidad_por_habitacion(self, id_habitacion: int) -> int:

        consulta = """
            SELECT th.capacidad
            FROM habitacion h
            JOIN tipo_habitacion th ON h.id_tipo_habitacion = th.id_tipo_habitacion
            WHERE h.id_habitacion = %s
        """

        valores = (id_habitacion, )
        resultado = self.obtener_dato_por_id(consulta, valores)
        
        
        if resultado:
            return int(resultado[0]) 
        return 0