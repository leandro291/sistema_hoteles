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

        self.frame_superior = tk.Frame(self.root, background="#6B6868")
        self.frame_superior.pack(side=tk.TOP, fill="x")

        tk.Label(self.frame_superior, text="HOTEL SYSTEM MANAGEMENT BETA V.1.00", background="#6B6868" , 
                font=("Arial", 35, "bold")).pack(pady=30
        )

        self.frame_main = tk.Frame(self.root, background="#F3DCAB")
        self.frame_main.pack(side=tk.TOP, fill="x")

        self.menu_opciones()
    
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
    
    def cargar_icono(self, nombre_archivo):

        carpeta_vistas = os.path.dirname(__file__)
        carpeta_raiz = os.path.dirname(carpeta_vistas)
        ruta_imagen = os.path.join(carpeta_raiz, 'assets', 'dashboard', nombre_archivo)

        try:
            imagen_original = Image.open(ruta_imagen)
            imagen_redimensionada = imagen_original.resize((100, 100))
            return ImageTk.PhotoImage(imagen_redimensionada)
        except FileNotFoundError:
            print(f"Error: No se encontró la imagen {nombre_archivo}")
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

        