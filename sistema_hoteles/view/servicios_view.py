import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from controllers.servicio_controller import ServicioController
from controllers.consumo_controller import ConsumoController

class ServiciosView:
    def __init__(self, root, manager):
        self.root = root
        self.manager = manager
        
        # Memoria RAM nativa para no consultar la BD en cada clic
        self.datos_servicios_memoria = [] 
        self.ids_reservas_memoria = []
        self.precio_unitario_actual = 0.0
        
        self.configurar_interfaz()
        
        # Carga inicial de datos (Descomentar cuando conectes los controladores)
        self.cargar_combobox_reservas()
        self.cargar_combobox_servicios()

    def configurar_interfaz(self):
        # --- HEADER ---
        self.frame_header = tk.Frame(self.root, background="#E0E0E0", bd=2, relief="groove")
        self.frame_header.pack(side=tk.TOP, fill="x")

        self.btn_volver = tk.Button(
            self.frame_header, text="⬅ Volver", font=("Arial", 16, "bold"), 
            bg="#555555", fg="white", relief="raised", padx=10, 
            command=self.manager.mostrar_dashboard
        )
        self.btn_volver.pack(side=tk.LEFT, padx=15, pady=15)
        
        tk.Label(
            self.frame_header, text="CARGOS Y SERVICIOS EXTRA", background="#E0E0E0", 
            font=("Arial", 28, "bold"), fg="#333333"
        ).pack(side=tk.LEFT, padx=20, pady=15)

        # --- CONTENEDOR PRINCIPAL (2 COLUMNAS) ---
        self.frame_main = tk.Frame(self.root, background="#F3DCAB")
        self.frame_main.pack(fill="both", expand=True, padx=20, pady=20)

        # =====================================================================
        # COLUMNA IZQUIERDA: REGISTRO DEL CONSUMO (FIJA)
        # =====================================================================
        self.panel_izquierda = tk.LabelFrame(
            self.frame_main, text=" Registrar Nuevo Cargo ", font=("Arial", 20, "bold"), 
            background="#F3DCAB", fg="#00838F", bd=2, relief="solid"
        )
        self.panel_izquierda.pack(side=tk.LEFT, fill="y", expand=False, ipadx=10, ipady=10, padx=(0, 15))

        # 1. Selección de Reserva (Habitación)
        tk.Label(self.panel_izquierda, text="Seleccionar Reserva Activa:", bg="#F3DCAB", fg="#00838F", font=("Arial", 16, "bold")).pack(anchor="w", padx=15, pady=(15, 2))
        self.lista_reservas = ttk.Combobox(self.panel_izquierda, font=("Arial", 16), state="readonly", width=25)
        self.lista_reservas.pack(padx=15, pady=(0, 15))
        self.lista_reservas.bind("<<ComboboxSelected>>", self.cargar_consumos_de_reserva)

        # 2. Selección de Servicio y Botón de Nuevo Servicio
        tk.Label(self.panel_izquierda, text="Catálogo de Servicios:", bg="#F3DCAB", fg="#00838F", font=("Arial", 16, "bold")).pack(anchor="w", padx=15, pady=(5, 2))
        
        frame_combo_servicio = tk.Frame(self.panel_izquierda, bg="#F3DCAB")
        frame_combo_servicio.pack(fill="x", padx=15, pady=(0, 15))

        self.lista_servicios = ttk.Combobox(frame_combo_servicio, font=("Arial", 16), state="readonly", width=18)
        self.lista_servicios.pack(side=tk.LEFT)
        self.lista_servicios.bind("<<ComboboxSelected>>", self.actualizar_precio_unitario)

        self.btn_nuevo_servicio = tk.Button(
            frame_combo_servicio, text="➕ Nuevo", font=("Arial", 10, "bold"), 
            bg="#1565C0", fg="white", command=self.abrir_modal_nuevo_servicio
        )
        self.btn_nuevo_servicio.pack(side=tk.LEFT, padx=(10, 0), ipady=2)

        # 3. Precio Unitario (Visual)
        self.lbl_precio = tk.Label(
            self.panel_izquierda, text="Precio Unitario: $0.00", 
            bg="#FFF3CD", fg="#856404", font=("Arial", 14, "bold"), relief="solid", bd=1
        )
        self.lbl_precio.pack(fill="x", padx=15, pady=(0, 15), ipadx=5, ipady=5)

        # 4. Cantidad
        tk.Label(self.panel_izquierda, text="Cantidad:", bg="#F3DCAB", fg="#00838F", font=("Arial", 16, "bold")).pack(anchor="w", padx=15, pady=(5, 2))
        self.spin_cantidad = ttk.Spinbox(self.panel_izquierda, from_=1, to=100, font=("Arial", 16), width=23)
        self.spin_cantidad.set(1)
        self.spin_cantidad.pack(padx=15, pady=(0, 15))
        
        # Eventos para recalcular el subtotal en vivo
        self.spin_cantidad.bind("<KeyRelease>", self.calcular_subtotal_vivo)
        self.spin_cantidad.bind("<<Increment>>", self.calcular_subtotal_vivo)
        self.spin_cantidad.bind("<<Decrement>>", self.calcular_subtotal_vivo)

        # 5. Subtotal Calculado
        self.lbl_subtotal = tk.Label(
            self.panel_izquierda, text="Subtotal: $0.00", 
            bg="#D4EDDA", fg="#155724", font=("Arial", 18, "bold"), relief="solid", bd=1
        )
        self.lbl_subtotal.pack(fill="x", padx=15, pady=(0, 20), ipadx=5, ipady=5)

        # Botón Guardar Transacción
        self.btn_guardar = tk.Button(
            self.panel_izquierda, text="💳 Agregar a la Cuenta", font=("Arial", 16, "bold"), 
            bg="#21DF96", fg="white", bd=2, relief="raised", command=self.ejecutar_transaccion
        )
        self.btn_guardar.pack(fill="x", side=tk.BOTTOM, padx=15, pady=15, ipady=5)


        # COLUMNA DERECHA: ESTADO DE CUENTA (EXPANDIBLE)
        self.panel_derecha = tk.LabelFrame(
            self.frame_main, text=" Detalle de Consumos de la Reserva ", font=("Arial", 20, "bold"), 
            background="#F3DCAB", fg="#00838F", bd=2, relief="solid"
        )
        self.panel_derecha.pack(side=tk.LEFT, fill="both", expand=True, ipadx=10, ipady=10)

        # Tabla de consumos
        estilo = ttk.Style()
        estilo.configure("Treeview.Heading", font=("Arial", 12, "bold"))
        estilo.configure("Treeview", font=("Arial", 12), rowheight=30)

        columnas = ("ID Cargo", "Servicio", "Precio Unit.", "Cantidad", "Subtotal")
        self.tabla_consumos = ttk.Treeview(self.panel_derecha, columns=columnas, show="headings", height=10)
        self.tabla_consumos.pack(fill="both", expand=True, padx=15, pady=(15, 5))

        self.tabla_consumos.heading("ID Cargo", text="ID Cargo")
        self.tabla_consumos.column("ID Cargo", width=80, anchor="center")
        self.tabla_consumos.heading("Servicio", text="Servicio")
        self.tabla_consumos.column("Servicio", width=250)
        self.tabla_consumos.heading("Precio Unit.", text="Precio Unit.")
        self.tabla_consumos.column("Precio Unit.", width=100, anchor="center")
        self.tabla_consumos.heading("Cantidad", text="Cantidad")
        self.tabla_consumos.column("Cantidad", width=80, anchor="center")
        self.tabla_consumos.heading("Subtotal", text="Subtotal")
        self.tabla_consumos.column("Subtotal", width=100, anchor="center")

        # Total acumulado y botón de eliminar
        self.frame_inferior_derecho = tk.Frame(self.panel_derecha, bg="#F3DCAB")
        self.frame_inferior_derecho.pack(fill="x", padx=15, pady=10)

        self.btn_quitar = tk.Button(
            self.frame_inferior_derecho, text="Anular Cargo Seleccionado", font=("Arial", 12, "bold"), 
            bg="#D32F2F", fg="white", command=self.anular_cargo
        )
        self.btn_quitar.pack(side=tk.LEFT)

        self.lbl_total_cuenta = tk.Label(
            self.frame_inferior_derecho, text="Total Extra: $0.00", 
            bg="#1565C0", fg="white", font=("Arial", 18, "bold"), padx=10, pady=5
        )
        self.lbl_total_cuenta.pack(side=tk.RIGHT)

    # Modal para agregar servicios
    def abrir_modal_nuevo_servicio(self):
        self.modal = tk.Toplevel(self.root)
        self.modal.title("Agregar Nuevo Servicio al Catálogo")
        self.modal.geometry("500x500")
        self.modal.resizable(False, False)
        self.modal.config(bg="#F3DCAB")        

        tk.Label(self.modal, text="Registro de Servicio", font=("Arial", 35, "bold"), bg="#F3DCAB").pack(pady=15)

        self.frame_form = tk.Frame(self.modal, bg="#F3DCAB")
        self.frame_form.pack(fill="both", expand=True, padx=20)

        tk.Label(self.frame_form, text="Nombre del Servicio:", font=("Arial", 25, "bold"), bg="#F3DCAB").pack(anchor="w")
        self.nombre = tk.Entry(self.frame_form, font=("Arial", 20), width=30)
        self.nombre.pack(pady=(0, 10))

        tk.Label(self.frame_form, text="Precio ($):", font=("Arial", 25, "bold"), bg="#F3DCAB").pack(anchor="w")
        self.precio = tk.Entry(self.frame_form, font=("Arial", 20), width=30)
        self.precio.pack(pady=(0, 10))

        tk.Label(self.frame_form, text="Descripción:", font=("Arial", 25, "bold"), bg="#F3DCAB").pack(anchor="w")
        self.descripcion = tk.Entry(self.frame_form, font=("Arial", 20), width=30)
        self.descripcion.pack(pady=(0, 15))

        tk.Button(
            self.modal, text="Guardar Servicio", font=("Arial", 28, "bold"), 
            bg="#21DF96", fg="white", command=self.guardar_nuevo_servicio
        ).pack(pady=20, fill="x", padx=20, ipady=20)

    def guardar_nuevo_servicio(self):
        
        nombre = self.nombre.get().strip()
        precio = self.precio.get().strip()
        descripcion = self.descripcion.get().strip()

        try:
            
            if not nombre: 
                raise ValueError("El nombre es obligatorio.")
            
            if not precio: 
                raise ValueError("Debe ingresar un precio.")
            
            controller = ServicioController()
            controller.registrar_nuevo_servicio(nombre, descripcion, precio)

    
            messagebox.showinfo("Exito", "Servicio agregado al catalogo")
            self.cargar_combobox_servicios() 
            self.modal.destroy() 
            
        except ValueError as ve:
            messagebox.showwarning("Dato Inválido", str(ve))
        except Exception as e:
            messagebox.showerror("Error de BD", str(e))
    
    def cargar_combobox_reservas(self):
        self.ids_reservas_memoria.clear()
        
        try:

            controller = ServicioController()

            bd_reservas = controller.obtener_todas_las_reservas_en_curso()

            if not bd_reservas:
                self.lista_reservas['values'] = ["No hay reservas en curso"]
                self.lista_reservas.current(0)
                return

            visual = []
            for fila in bd_reservas:
                
                self.ids_reservas_memoria.append(fila[0])
                
                texto_amigable = f"Hab. {fila[1]} - {fila[2]} {fila[3]}"
                visual.append(texto_amigable)

            self.lista_reservas['values'] = visual
            self.lista_reservas.current(0)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las reservas: {e}")
        
    def cargar_combobox_servicios(self):
        self.datos_servicios_memoria.clear()

        try:
            
            controller = ServicioController()
            
            # Traemos los datos de la BD
            bd_servicios = controller.obtener_todos_los_servicios()

            # Validamos si la tabla está vacía
            if not bd_servicios:
                self.lista_servicios['values'] = ["Sin servicios disponibles"]
                self.lista_servicios.current(0)
                self.lbl_precio.config(text="Precio Unitario: $0.00")
                return

            visual = []
            for fila in bd_servicios:
            
                self.datos_servicios_memoria.append({
                    "id": fila[0], 
                    "nombre": fila[1], 
                    "precio": float(fila[3]) 
                })
                
                visual.append(fila[1])

            self.lista_servicios['values'] = visual
            self.lista_servicios.current(0) 
            self.actualizar_precio_unitario()

        except Exception as e:
            messagebox.showerror("Error Crítico de BD", f"No se pudo cargar el catálogo de servicios:\n{e}")

    def actualizar_precio_unitario(self, event=None):
        idx = self.lista_servicios.current()
        if idx >= 0 and self.datos_servicios_memoria:
            servicio_seleccionado = self.datos_servicios_memoria[idx]
            self.precio_unitario_actual = servicio_seleccionado["precio"]
            self.lbl_precio.config(text=f"Precio Unitario: ${self.precio_unitario_actual:.2f}")
            self.calcular_subtotal_vivo()

    def calcular_subtotal_vivo(self, event=None):
        try:
            cantidad = int(self.spin_cantidad.get())
            if cantidad < 1: 
                self.lbl_subtotal.config(text="Subtotal: $0.00")
                return
            subtotal = self.precio_unitario_actual * cantidad
            self.lbl_subtotal.config(text=f"Subtotal: ${subtotal:.2f}")
        except ValueError:
            self.lbl_subtotal.config(text="Subtotal: $0.00")

    def cargar_consumos_de_reserva(self, event=None):
        # Limpiar la tabla de registros anteriores 
        for item in self.tabla_consumos.get_children():
            self.tabla_consumos.delete(item)

        # Verificar qué reserva está seleccionada en el Combobox izquierdo
        idx_reserva = self.lista_reservas.current()
        
        # Si no hay nada seleccionado, dejamos el total en cero y cortamos la ejecución
        if idx_reserva == -1 or not self.ids_reservas_memoria:
            self.lbl_total_cuenta.config(text="Total Extra: $0.00")
            return

        # Extraer el ID real de la base de datos desde tu memoria RAM
        id_reserva_real = self.ids_reservas_memoria[idx_reserva]

        try:
            # Instanciar el controlador y pedirle los datos (esto ejecutará el fetchall)
            controller = ConsumoController()
            
            # Esto devuelve la lista de tuplas desde SQL Server
            consumos = controller.obtener_historial_consumos(id_reserva_real) 

            total_extra = 0.0

            # Iterar sobre los resultados e insertarlos en el Treeview
            if consumos:
                for fila in consumos:
                    # Desempaquetamos la tupla según el orden del SELECT que hicimos en el DAO
                    id_cargo = fila[0]
                    nombre = fila[1]
                    precio = f"${float(fila[2])}"
                    cantidad = fila[3]
                    subtotal_num = float(fila[4])
                    subtotal_str = f"${subtotal_num:.2f}"
                    
                    # Insertamos la fila visualmente en la tabla blanca
                    self.tabla_consumos.insert("", "end", values=(id_cargo, nombre, precio, cantidad, subtotal_str))
                    
                    # Acumulamos el subtotal matemático para el gran total
                    total_extra += subtotal_num

            # Actualizar el recuadro azul de la esquina inferior derecha
            self.lbl_total_cuenta.config(text=f"Total Extra: ${total_extra:.2f}")

        except Exception as e:
            messagebox.showerror("Error de Carga", f"Fallo al traer los detalles de consumo: {e}")

    def ejecutar_transaccion(self):
        idx_reserva = self.lista_reservas.current()
        idx_servicio = self.lista_servicios.current()
        
        if idx_reserva == -1 or not self.ids_reservas_memoria:
            messagebox.showwarning("Aviso", "Debe tener al menos una reserva activa seleccionada.")
            return
            
        if idx_servicio == -1 or not self.datos_servicios_memoria:
            messagebox.showwarning("Aviso", "Debe seleccionar un servicio válido del catálogo.")
            return
            
        try:
            cantidad = int(self.spin_cantidad.get())
            if cantidad < 1:
                raise ValueError("La cantidad debe ser 1 o mayor.")

            # Extracción segura
            id_reserva_real = self.ids_reservas_memoria[idx_reserva]
            id_servicio_real = self.datos_servicios_memoria[idx_servicio]["id"]
            
            controller = ConsumoController()
            id_generado = controller.registrar_servicio(
                id_servicio=id_servicio_real, 
                id_reserva=id_reserva_real, 
                cantidad=cantidad
            )
            
            messagebox.showinfo("Éxito", f"Cargo registrado correctamente. (Ticket ID: {id_generado})")
            
            self.spin_cantidad.set(1)
            self.calcular_subtotal_vivo() 
            self.cargar_consumos_de_reserva() 
            
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error de BD", str(e))
            
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero válido.")
        except Exception as e:
            messagebox.showerror("Error de BD", str(e))

    def anular_cargo(self):
        seleccionado = self.tabla_consumos.selection()
        if not seleccionado: 
            messagebox.showwarning("Aviso", "Seleccione un cargo de la tabla para anularlo.")
            return
        
        valores = self.tabla_consumos.item(seleccionado[0])['values']
        id_cargo_real = valores[0]
        nombre_servicio = valores[1]

        if messagebox.askyesno("Confirmar Anulación", f"¿Está seguro de anular el cargo por '{nombre_servicio}'?"):
            try:
                controller = ConsumoController()
                controller.eliminar_consumo(id_cargo_real)
                
                messagebox.showinfo("Éxito", "Cargo anulado correctamente.")
                
                self.cargar_consumos_de_reserva()
                
            except Exception as e:
                messagebox.showerror("Error de BD", f"No se pudo anular el cargo en la base de datos:\n{e}")