import tkinter as tk
from tkinter import ttk # OBLIGATORIO: Para poder usar las listas desplegables (Combobox)

class HabitacionView:
    def __init__(self, root, manager):
        self.root = root
        self.manager = manager
        self.configurar_interfaz()

    def configurar_interfaz(self):

        self.frame_header = tk.Frame(self.root, background="#E0E0E0", bd=2, relief="groove")
        self.frame_header.pack(side=tk.TOP, fill="x")

        self.btn_volver = tk.Button(
            self.frame_header, text="⬅ Volver al Inicio", font=("Arial", 12, "bold"), 
            bg="#555555", fg="white", command=self.manager.mostrar_dashboard 
        )
        self.btn_volver.place(relx=0.02, rely=0.5, anchor="w")
        
        tk.Label(
            self.frame_header, text="HABITACIONES", background="#E0E0E0", 
            font=("Arial", 30, "bold"), fg="#333333"
        ).pack(pady=20)

        self.frame_main = tk.Frame(self.root, background="#F3DCAB")
        self.frame_main.pack(side=tk.TOP, fill="both", expand=True)

        self.frame_cuerpo = tk.Frame(self.frame_main, background="#F3DCAB")
        self.frame_cuerpo.pack(side=tk.TOP, fill="both", expand=True, padx=20, pady=10)

        self.panel_izquierdo = tk.Frame(self.frame_cuerpo, background="#F3DCAB", width=250)
        self.panel_izquierdo.pack(side=tk.LEFT, fill="y", padx=(0, 20))
        self.panel_izquierdo.pack_propagate(False) 

        self.caja_lista = tk.Frame(self.panel_izquierdo, background="#F4EADB", bd=1, relief="solid")
        self.caja_lista.pack(side=tk.LEFT, fill="both", expand=True)
        
        self.scroll_lista = tk.Scrollbar(self.panel_izquierdo)
        self.scroll_lista.pack(side=tk.RIGHT, fill="y")

        self.panel_derecho = tk.Frame(self.frame_cuerpo, background="#F3DCAB")
        self.panel_derecho.pack(side=tk.LEFT, fill="both", expand=True)

        self.caja_tabla = tk.Frame(self.panel_derecho, background="#D9D9D9", bd=1, relief="solid")
        self.caja_tabla.pack(side=tk.TOP, fill="both", expand=True, pady=(0, 15))

        self.franja_botones = tk.Frame(self.panel_derecho, background="#E0E0E0", bd=1, relief="solid")
        self.franja_botones.pack(side=tk.TOP, fill="x") 
        
        self.sub_frame_botones = tk.Frame(self.franja_botones, background="#E0E0E0")
        self.sub_frame_botones.pack(pady=10)

        self.btn_agregar = tk.Button(
            self.sub_frame_botones, text="Agregar Habitación", font=("Arial", 16, "bold"), fg="#21DF96",
            command=self.abrir_formulario_agregar_habitacion
        )
        self.btn_agregar.pack(side=tk.LEFT, padx=10)

        self.btn_editar = tk.Button(
            self.sub_frame_botones, text="Editar Habitación", font=("Arial", 16, "bold"), fg="#1565C0",
            command=self.editar_habitacion
        )
        self.btn_editar.pack(side=tk.LEFT, padx=10)

        self.btn_eliminar = tk.Button(
            self.sub_frame_botones, text="Eliminar Habitación", font=("Arial", 16, "bold"), fg="#C62828",
            command=self.eliminar_habitacion
        )
        self.btn_eliminar.pack(side=tk.LEFT, padx=10)


        self.btn_gestionar_tipos = tk.Button(
            self.sub_frame_botones, text="Configurar Tipos", font=("Arial", 16, "bold"), fg="#EF6C00",
            command=self.abrir_formulario_tipos
        )
        self.btn_gestionar_tipos.pack(side=tk.LEFT, padx=(40, 10))

    def abrir_formulario_tipos(self):
        ventana_tipos = tk.Toplevel(self.root)
        ventana_tipos.title("Configurar Tipos de Habitación")
        ventana_tipos.geometry("500x600")
        ventana_tipos.resizable(False, False)
        ventana_tipos.configure(background="#F3DCAB")

        tk.Label(
            ventana_tipos, text="CATÁLOGO DE TIPOS", bg="#F3DCAB", 
            font=("Arial", 30, "bold"), pady=10
        ).pack(fill="x", side=tk.TOP, pady=(0, 20))


        tk.Label(ventana_tipos, text="Nombre:", bg="#F3DCAB", font=("Arial", 25, "bold")).pack(anchor="w", padx=40)
        self.tipo_hab_nombre = tk.Entry(ventana_tipos, font=("Arial", 22), bd=1, relief="solid")
        self.tipo_hab_nombre.pack(fill="x", padx=40, pady=(0, 15))

        # 2. Precio
        tk.Label(ventana_tipos, text="Precio:", bg="#F3DCAB", font=("Arial", 25, "bold")).pack(anchor="w", padx=40)
        self.tipo_hab_precio = tk.Entry(ventana_tipos, font=("Arial", 22), bd=1, relief="solid")
        self.tipo_hab_precio.pack(fill="x", padx=40, pady=(0, 15))

        tk.Label(ventana_tipos, text="Capacidad de Personas:", bg="#F3DCAB", font=("Arial", 25, "bold")).pack(anchor="w", padx=40)
        self.tipo_hab_capacidad = tk.Spinbox(ventana_tipos, from_=1, to=10, font=("Arial", 22), bd=1, relief="solid")
        self.tipo_hab_capacidad.pack(fill="x", padx=40, pady=(0, 15))

        tk.Label(ventana_tipos, text="Descripción:", bg="#F3DCAB", font=("Arial", 25, "bold")).pack(anchor="w", padx=40)
        self.tipo_hab_descripcion = tk.Entry(ventana_tipos, font=("Arial", 22), bd=1, relief="solid")
        self.tipo_hab_descripcion.pack(fill="x", padx=40, pady=(0, 25))

        self.btn_guardar_tipo = tk.Button(
            ventana_tipos, text="Guardar Nuevo Tipo", bg="#ffffff", fg="#40e794", 
            font=("Arial", 20, "bold"), bd=2, relief="raised"
        )
        self.btn_guardar_tipo.pack(fill="x", padx=40)

    def obtener_formulario_tipos(self):
        pass

    def editar_habitacion(self):
        pass

    def eliminar_habitacion(self):
        pass