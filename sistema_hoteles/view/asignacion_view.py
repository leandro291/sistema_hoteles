import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from models.reserva import Reserva
from models.acompanante import Acompanante
from controllers.recepcion_controller import RecepcionController
from controllers.cliente_controller import ClienteController
from controllers.habitacion_controller import HabitacionController

class AsignacionView:
    def __init__(self, root, manager):
        self.root = root
        self.manager = manager
        
        # Memoria ram para las transacciones
        self.lista_acompanantes_memoria = []
        self.ids_clientes_memoria = []
        
        # Guardar numero, id y capacidad de  las habitaciones
        self.datos_habitaciones = [] 
        self.capacidad_actual_seleccionada = 0
        
        self.configurar_interfaz()
        self.cargar_combobox_clientes()
        self.cargar_combobox_habitaciones()

    def configurar_interfaz(self):
        # --- HEADER ---
        self.frame_header = tk.Frame(self.root, background="#E0E0E0", bd=2, relief="groove")
        self.frame_header.pack(side=tk.TOP, fill="x")

        self.btn_volver = tk.Button(
            self.frame_header, text="⬅ Volver", font=("Arial", 16, "bold"), 
            bg="#555555", fg="white", relief="raised", padx=10, command=self.manager.mostrar_dashboard
        )
        self.btn_volver.pack(side=tk.LEFT, padx=15, pady=15)
        
        tk.Label(
            self.frame_header, text="ASIGNACIÓN DE HABITACIONES", background="#E0E0E0", 
            font=("Arial", 28, "bold"), fg="#333333"
        ).pack(side=tk.LEFT, padx=20, pady=15)

        # --- CONTENEDOR PRINCIPAL (2 COLUMNAS) ---
        self.frame_main = tk.Frame(self.root, background="#F3DCAB")
        self.frame_main.pack(fill="both", expand=True, padx=20, pady=20)

        # =====================================================================
        # COLUMNA IZQUIERDA: DATOS DE RESERVA
        # =====================================================================
        self.panel_izquierda = tk.LabelFrame(
            self.frame_main, text=" Datos del Check-In ", font=("Arial", 20, "bold"), 
            background="#F3DCAB", fg="#00838F", bd=2, relief="solid"
        )
        self.panel_izquierda.pack(side=tk.LEFT, fill="y", expand=False, ipadx=10, ipady=10, padx=(0, 15))

        tk.Label(self.panel_izquierda, text="Cliente Titular:", bg="#F3DCAB", fg="#00838F", font=("Arial", 16, "bold")).pack(anchor="w", padx=15, pady=(15, 2))
        self.lista_clientes = ttk.Combobox(self.panel_izquierda, font=("Arial", 16), state="readonly", width=25)
        self.lista_clientes.pack(padx=15, pady=(0, 15))

        tk.Label(self.panel_izquierda, text="Seleccionar Habitación:", bg="#F3DCAB", fg="#00838F", font=("Arial", 16, "bold")).pack(anchor="w", padx=15, pady=(5, 2))
        self.lista_habitaciones = ttk.Combobox(self.panel_izquierda, font=("Arial", 16), state="readonly", width=25)
        self.lista_habitaciones.pack(padx=15, pady=(0, 5))
        
        self.lista_habitaciones.bind("<<ComboboxSelected>>", self.actualizar_capacidad_visual)

        self.lbl_capacidad = tk.Label(
            self.panel_izquierda, text="Capacidad: Seleccione un cuarto", 
            bg="#FFF3CD", fg="#856404", font=("Arial", 12, "bold"), relief="solid", bd=1
        )
        self.lbl_capacidad.pack(fill="x", padx=15, pady=(0, 15), ipadx=5, ipady=5)

        tk.Label(self.panel_izquierda, text="Fecha Ingreso:", bg="#F3DCAB", fg="#00838F", font=("Arial", 16, "bold")).pack(anchor="w", padx=15, pady=(5, 2))
        self.ingreso = tk.Entry(self.panel_izquierda, font=("Arial", 16), width=26, bd=1, relief="solid")
        self.ingreso.pack(padx=15, pady=(0, 15))
        self.ingreso.insert(0, "YYYY-MM-DD")

        tk.Label(self.panel_izquierda, text="Fecha Salida:", bg="#F3DCAB", fg="#00838F", font=("Arial", 16, "bold")).pack(anchor="w", padx=15, pady=(5, 2))
        self.salida = tk.Entry(self.panel_izquierda, font=("Arial", 16), width=26, bd=1, relief="solid")
        self.salida.pack(padx=15, pady=(0, 20))
        self.salida.insert(0, "YYYY-MM-DD")

        self.btn_guardar = tk.Button(
            self.panel_izquierda, text="Confirmar y Guardar", font=("Arial", 18, "bold"), 
            bg="#21DF96", fg="white", bd=2, relief="raised", command=self.ejecutar_transaccion
        )
        self.btn_guardar.pack(fill="x", side=tk.BOTTOM, padx=15, pady=15, ipady=5)

        # =====================================================================
        # COLUMNA DERECHA: GESTIÓN INTELIGENTE DE ACOMPAÑANTES
        # =====================================================================
        self.panel_derecha = tk.LabelFrame(
            self.frame_main, text=" Registro de Acompañantes ", font=("Arial", 20, "bold"), 
            background="#F3DCAB", fg="#00838F", bd=2, relief="solid"
        )
        self.panel_derecha.pack(side=tk.LEFT, fill="both", expand=True, ipadx=10, ipady=10)

        self.frame_form_acomp = tk.Frame(self.panel_derecha, bg="#E0E0E0", bd=1, relief="solid")
        self.frame_form_acomp.pack(fill="x", padx=15, pady=15)

        tk.Label(self.frame_form_acomp, text="Nombre:", bg="#E0E0E0", font=("Arial", 14, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=(10,0))
        self.acompanante_nombre = tk.Entry(self.frame_form_acomp, font=("Arial", 14), width=15)
        self.acompanante_nombre.grid(row=1, column=0, padx=10, pady=(0,15))

        tk.Label(self.frame_form_acomp, text="Apellido:", bg="#E0E0E0", font=("Arial", 14, "bold")).grid(row=0, column=1, sticky="w", padx=10, pady=(10,0))
        self.acompanante_apellido = tk.Entry(self.frame_form_acomp, font=("Arial", 14), width=15)
        self.acompanante_apellido.grid(row=1, column=1, padx=10, pady=(0,15))

        tk.Label(self.frame_form_acomp, text="Documento:", bg="#E0E0E0", font=("Arial", 14, "bold")).grid(row=0, column=2, sticky="w", padx=10, pady=(10,0))
        self.acompanante_num_doc = tk.Entry(self.frame_form_acomp, font=("Arial", 14), width=15)
        self.acompanante_num_doc.grid(row=1, column=2, padx=10, pady=(0,15))

        tk.Label(self.frame_form_acomp, text="Teléfono:", bg="#E0E0E0", font=("Arial", 14, "bold")).grid(row=0, column=3, sticky="w", padx=10, pady=(10,0))
        self.acompanante_telefono = tk.Entry(self.frame_form_acomp, font=("Arial", 14), width=15)
        self.acompanante_telefono.grid(row=1, column=3, padx=10, pady=(0,15))

        self.btn_agregar = tk.Button(
            self.frame_form_acomp, text="Añadir a la Lista", font=("Arial", 12, "bold"), 
            bg="#1565C0", fg="white", command=self.agregar_acompanante_lista
        )
        self.btn_agregar.grid(row=1, column=4, padx=15, pady=(0,15), sticky="we")

        # Tabla
        estilo = ttk.Style()
        estilo.configure("Treeview.Heading", font=("Arial", 12, "bold"))
        estilo.configure("Treeview", font=("Arial", 12), rowheight=30)

        columnas = ("Nombre", "Apellido", "Documento", "Teléfono")
        self.tabla_acompanantes = ttk.Treeview(self.panel_derecha, columns=columnas, show="headings", height=10)
        self.tabla_acompanantes.pack(fill="both", expand=True, padx=15, pady=5)

        for col in columnas:
            self.tabla_acompanantes.heading(col, text=col)
            self.tabla_acompanantes.column(col, width=120)

        self.btn_quitar = tk.Button(
            self.panel_derecha, text="🗑️ Eliminar Seleccionado", font=("Arial", 14, "bold"), 
            bg="#D32F2F", fg="white", command=self.quitar_acompanante_lista
        )
        self.btn_quitar.pack(side=tk.RIGHT, padx=15, pady=15)


    # Logica de control y eventos

    def cargar_combobox_clientes(self):
        
        self.ids_clientes_memoria.clear()
        
        controller = ClienteController()

        bd_clientes = controller.obtener_todos_clientes()

        if not bd_clientes:
            self.lista_clientes['values'] = ["Sin clientes"]
            return

        visual = []
        for cliente in bd_clientes:
            self.ids_clientes_memoria.append(cliente[0])
            visual.append(f"{cliente[1]} - {cliente[2]}")
        
        self.lista_clientes['values'] = visual
        self.lista_clientes.current(0)

    def cargar_combobox_habitaciones(self):
        
        self.datos_habitaciones.clear()

        controller = HabitacionController()
        
        bd_habitaciones = controller.obtener_habitaciones_disponibles()
        
        if not bd_habitaciones:
            self.lista_habitaciones['values'] = ["Sin cuartos libres"]
            self.lbl_capacidad.config(text="No hay disponibilidad", bg="#F8D7DA", fg="#721C24")
            return

        visual = []
        for habitacion in bd_habitaciones:
            self.datos_habitaciones.append({"id": habitacion[0], "numero": habitacion[1], "capacidad": habitacion[2]})
            visual.append(f"Habitación {habitacion[1]} (Cap: {habitacion[2]})")

        self.lista_habitaciones['values'] = visual
        self.lista_habitaciones.current(0)
        
        self.actualizar_capacidad_visual(None)

    def actualizar_capacidad_visual(self, event):
        idx = self.lista_habitaciones.current()
        if idx == -1 or not self.datos_habitaciones:
            return
            
        hab_seleccionada = self.datos_habitaciones[idx]
        self.capacidad_actual_seleccionada = hab_seleccionada["capacidad"]
        
        max_acompanantes = self.capacidad_actual_seleccionada - 1 
        
        texto = f"Capacidad Total: {self.capacidad_actual_seleccionada} personas. (Máximo {max_acompanantes} acompañantes)"
        self.lbl_capacidad.config(text=texto, bg="#D4EDDA", fg="#155724")

    def agregar_acompanante_lista(self):
        max_acompanantes_permitidos = self.capacidad_actual_seleccionada - 1
        
        if len(self.lista_acompanantes_memoria) >= max_acompanantes_permitidos:
            messagebox.showerror(
                "Límite Excedido", 
                f"La habitación seleccionada solo permite {max_acompanantes_permitidos} acompañantes extra.\nEl titular ocupa 1 espacio."
            )
            return

        nombre = self.acompanante_nombre.get().strip()
        apellido = self.acompanante_apellido.get().strip()
        numero_doc = self.acompanante_num_doc.get().strip()
        telefono = self.acompanante_telefono.get().strip()

        if not nombre or not apellido or not numero_doc:
            messagebox.showwarning("Error", "Llene los datos obligatorios del acompañante.")
            return

        nuevo_acomp = {
            "nombre": nombre, 
            "apellido": apellido, 
            "tipo_documento": "DNI", 
            "num_documento": numero_doc, 
            "telefono": telefono
        }
        
        self.lista_acompanantes_memoria.append(nuevo_acomp)
        self.tabla_acompanantes.insert("", tk.END, values=(nombre, apellido, numero_doc, telefono))

        self.acompanante_nombre.delete(0, tk.END)
        self.acompanante_apellido.delete(0, tk.END)
        self.acompanante_num_doc.delete(0, tk.END)
        self.acompanante_telefono.delete(0, tk.END)

    def quitar_acompanante_lista(self):
        seleccionado = self.tabla_acompanantes.selection()

        if not seleccionado: 
            return
        
        item_id = seleccionado[0]
        self.lista_acompanantes_memoria.pop(self.tabla_acompanantes.index(item_id))
        self.tabla_acompanantes.delete(item_id)

    def ejecutar_transaccion(self):
        id_cliente = self.lista_clientes.current()
        id_habitacion = self.lista_habitaciones.current()
        
        if id_cliente == -1 or id_habitacion == -1: 
            return
            
        id_cliente_bd = self.ids_clientes_memoria[id_cliente]
        id_habitacion_bd = self.datos_habitaciones[id_habitacion]["id"]

        fecha_entrada = self.ingreso.get().strip()
        fecha_salida = self.salida.get().strip()

        try:

            datos_reserva = {
                "fecha_entrada": fecha_entrada,
                "fecha_salida": fecha_salida
            }

            selecciones = [{
                "id_habitacion": id_habitacion_bd, 
                "tiene_titular": True, 
                "acompanantes": self.lista_acompanantes_memoria
            }]

            controller = RecepcionController()
            controller.registrar_check_in(
                id_cliente=id_cliente_bd, 
                datos_reserva=datos_reserva, 
                id_usuario=2, 
                selecciones=selecciones
            )

            messagebox.showinfo("Éxito", "Check-In exitoso.")
            self.limpiar_formulario()
        except ValueError as e:
            messagebox.showerror("Datos Invalidos", str(e))
        except Exception as e:
            messagebox.showerror(f"Error Crítico de BD", e)

    def limpiar_formulario(self):
        self.ingreso.delete(0, tk.END); self.ingreso.insert(0, "YYYY-MM-DD")
        self.salida.delete(0, tk.END); self.salida.insert(0, "YYYY-MM-DD")
        self.lista_acompanantes_memoria.clear()

        for item in self.tabla_acompanantes.get_children(): 
            self.tabla_acompanantes.delete(item)

        self.cargar_combobox_habitaciones()
