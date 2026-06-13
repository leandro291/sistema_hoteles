import tkinter as tk
from PIL import Image, ImageTk

from utils import limpiar_ventana
import os

class DashboardView:
    def __init__(self, root, manager):
        self.root = root
        self.manager = manager

        self.configurar_intefaz()
    
    def configurar_intefaz(self):

        # Contenedor Superior del sistema
        self.frame_superior = tk.Frame(self.root, background="#6B6868")
        self.frame_superior.pack(side=tk.TOP, fill="x")

        tk.Label(self.frame_superior, text="HOTEL SYSTEM MANAGEMENT BETA V.1.00", background="#6B6868" , 
                font=("Arial", 35, "bold")).pack(pady=30
        )

        # Contenedor de submenus del sistema
        self.frame_main = tk.Frame(self.root, background="#F3DCAB")
        self.frame_main.pack(side=tk.TOP, fill="x")

        self.menu_opciones()

        # Contenedor del pie de pagina del sistema
        self.frame_footer = tk.Frame(self.root, background="#F3DCAB")
        self.frame_footer.pack(side=tk.TOP, fill="both", expand=True)

        self.registros_base_de_datos()
    
    def menu_opciones(self):

        self.contenedor_botones = tk.Frame(self.frame_main, background="#F3DCAB")
        self.contenedor_botones.pack(pady=40)

        self.icono_habitacion = self.cargar_icono('logo_habitacion.webp')
        self.icono_asignacion = self.cargar_icono('logo_asignacion.webp')
        self.icono_clientes = self.cargar_icono('logo_clientes.webp')
        self.icono_pagos = self.cargar_icono('logo_pago.webp')
        self.icono_informacion = self.cargar_icono('logo_informacion.webp')

        self.boton_habitacion = self.modelo_botones("Habitaciones", self.icono_habitacion)
        self.boton_asignacion = self.modelo_botones("Asignaciones", self.icono_asignacion)
        self.boton_clientes   = self.modelo_botones("Clientes", self.icono_clientes)
        self.boton_pago       = self.modelo_botones("Pagos", self.icono_pagos)
        self.boton_informacion= self.modelo_botones("Información", self.icono_informacion)

    def registros_base_de_datos(self):

        self.vista_datos = tk.Frame(self.frame_footer, background="#F3DCAB")
        self.vista_datos.pack(side=tk.LEFT, expand=True, fill="both")
        self.vista_datos.pack_propagate(False)

        tk.Label(self.vista_datos, text="Reporte de gestion del hotel", background="#F3DCAB" , 
                font=("Arial", 25, "bold")).pack()
        
        self.contenedor_tarjetas = tk.Frame(self.vista_datos, background="#F3DCAB")
        self.contenedor_tarjetas.pack(pady=30)
        
        self.total_habitaciones = self.crear_tarjetas_datos("Total de\n Habitaciones", 0)
        self.habitaciones_disponibles = self.crear_tarjetas_datos("Habitaciones\n Disponibles", 0)
        self.habitaciones_ocupadas = self.crear_tarjetas_datos("Habitaciones\n Ocupadas", 0)
        self.total_clientes = self.crear_tarjetas_datos("Total de\n Clientes", 0)

        self.boton_registrar = tk.Button(self.vista_datos, text="Actualizar reporte", font=("Arial", 20, "bold"), bd=2, relief="raised")
        self.boton_registrar.pack()

        self.vista_imagen = tk.Frame(self.frame_footer, background="#F3DCAB")
        self.vista_imagen.pack(side=tk.LEFT, expand=True, fill="both")
        self.vista_imagen.pack_propagate(False)

        carpeta_vistas = os.path.dirname(__file__)
        carpeta_raiz = os.path.dirname(carpeta_vistas)
        ruta_imagen = os.path.join(carpeta_raiz, 'assets', 'login', 'logo.webp')

        imagen_original = Image.open(ruta_imagen)
        imagen_redimensionada = imagen_original.resize((500, 350))
        self.logo_imagen = ImageTk.PhotoImage(imagen_redimensionada)

        tk.Label(self.vista_imagen, image=self.logo_imagen).pack()
        
    def crear_tarjetas_datos(self, titulo, valor_inicial):
        tarjeta = tk.Frame(self.contenedor_tarjetas, background="white", width=150, height=180)
        tarjeta.pack(side=tk.LEFT, padx=10)
        tarjeta.pack_propagate(False)
        
        tk.Label(
            tarjeta, text=titulo, background="#21DF96", foreground="#ffffff", 
            font=("Arial", 14, "bold"), pady=10
        ).pack(side=tk.TOP, fill="x")
        
        label_numero = tk.Label(
            tarjeta, text=valor_inicial, background="#ffffff", foreground="#21DF96", 
            font=("Arial", 50, "bold"), pady=15
        )
        label_numero.pack(expand=True, fill="both")

        return label_numero
    
    def cargar_icono(self, nombre_archivo):

        carpeta_vistas = os.path.dirname(__file__)
        carpeta_raiz = os.path.dirname(carpeta_vistas)
        ruta_imagen = os.path.join(carpeta_raiz, 'assets', 'dashboard', nombre_archivo)

        try:
            imagen_original = Image.open(ruta_imagen)
            imagen_redimensionada = imagen_original.resize((100, 100))
            return ImageTk.PhotoImage(imagen_redimensionada)
        except FileNotFoundError:
            print(f"No se encontro la imagen {nombre_archivo}")
            return tk.PhotoImage()

    def modelo_botones(self, text, image, command=None):
        boton = tk.Button(
            self.contenedor_botones, text=text, image=image, 
            compound=tk.TOP, font=("Arial", 20, "bold"), bd=2, relief="raised",
            width=220, height=180, command=command
        )
        boton.pack(side=tk.LEFT, pady=10, padx=15)

        return boton

    def cerrar_sesion(self):
        limpiar_ventana(self.root)

        