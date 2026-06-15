import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from controllers.servicio_controller import ServicioController
from controllers.caja_controller import CajaController

class PagoView:
    def __init__(self, root, manager):
        self.root = root
        self.manager = manager

        self.ids_reservas_modal_memoria = []

        self.configurar_interfaz()
        
        # Disparador automático activado: Llena la tabla al instante de abrir la vista
        self.cargar_datos_pagos()

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
            self.frame_header, text="REGISTRO Y DETALLE DE PAGOS", background="#E0E0E0", 
            font=("Arial", 28, "bold"), fg="#333333"
        ).pack(side=tk.LEFT, padx=20, pady=15)

        # --- CONTENEDOR PRINCIPAL ---
        self.frame_main = tk.Frame(self.root, background="#F3DCAB")
        self.frame_main.pack(fill="both", expand=True, padx=20, pady=20)

        # PANEL CENTRAL: TABLA DE HISTORIAL 
        self.panel_tabla = tk.LabelFrame(
            self.frame_main, text=" Historial General de Pagos ", font=("Arial", 20, "bold"), 
            background="#F3DCAB", fg="#00838F", bd=2, relief="solid"
        )
        self.panel_tabla.pack(fill="both", expand=True, ipadx=10, ipady=10)

        estilo = ttk.Style()
        estilo.configure("Treeview.Heading", font=("Arial", 12, "bold"))
        estilo.configure("Treeview", font=("Arial", 12), rowheight=30)

        columnas = (
            "ID Pago", "Fecha de Pago", "Reserva / Cliente", 
            "Monto Total", "Método", "Comprobante", 
            "Estado", "Atendido Por"
        )
        
        self.tabla_pagos = ttk.Treeview(self.panel_tabla, columns=columnas, show="headings", height=15)
        
        scroll_y = ttk.Scrollbar(self.panel_tabla, orient="vertical", command=self.tabla_pagos.yview)
        scroll_y.pack(side="right", fill="y")
        
        scroll_x = ttk.Scrollbar(self.panel_tabla, orient="horizontal", command=self.tabla_pagos.xview)
        scroll_x.pack(side="bottom", fill="x")
        
        self.tabla_pagos.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.tabla_pagos.pack(fill="both", expand=True, padx=(15, 0), pady=(15, 0))

        anchos = {
            "ID Pago": 80, "Fecha de Pago": 150, "Reserva / Cliente": 300, 
            "Monto Total": 100, "Método": 100, "Comprobante": 120, 
            "Estado": 100, "Atendido Por": 150
        }

        for col in columnas:
            self.tabla_pagos.heading(col, text=col)
            self.tabla_pagos.column(col, width=anchos[col], anchor="center")
            
        self.tabla_pagos.column("Reserva / Cliente", anchor="w")

        # PANEL INFERIOR: ACCIONES DE FACTURACIÓN
        self.frame_acciones = tk.Frame(self.frame_main, bg="#F3DCAB")
        self.frame_acciones.pack(fill="x", pady=(10, 0))

        self.btn_nuevo_cobro = tk.Button(
            self.frame_acciones, text="Registrar Nuevo Cobro", 
            font=("Arial", 16, "bold"), bg="#21DF96", fg="white", 
            bd=3, relief="raised", padx=20, pady=5,
            command=self.abrir_modal_cobro
        )
        self.btn_nuevo_cobro.pack(side=tk.RIGHT, padx=15)


    #Metodos de logica y conexion

    def cargar_datos_pagos(self):
        for item in self.tabla_pagos.get_children():
            self.tabla_pagos.delete(item)

        try:
            controller = CajaController()
            pagos = controller.obtener_todos_los_pagos()

            if pagos:
                for item in pagos:
                    id_pago = item[0]
                    fecha = item[1]
                    cliente = item[2]
                    monto = f"${float(item[3]):.2f}"
                    metodo = item[4]
                    comprobante = item[5]
                    estado = item[6]
                    usuario = item[7]
                    
                    
                    self.tabla_pagos.insert("", "end", values=(
                        id_pago, fecha, cliente, monto, metodo, comprobante, estado, usuario
                    ))

        except Exception as e:
            messagebox.showerror("Error de BD", f"Error cargando historial:\n{e}")

    def abrir_modal_cobro(self):
        self.modal = tk.Toplevel(self.root)
        self.modal.title("Liquidación y Cobro de Habitación")
        self.modal.geometry("550x650")
        self.modal.resizable(False, False)
        self.modal.config(bg="#F3DCAB")
        
        self.modal.grab_set()

        tk.Label(self.modal, text="Liquidar Habitación", font=("Arial", 26, "bold"), bg="#F3DCAB", fg="#00838F").pack(pady=(20, 10))

        # =========================================================
        # ZONA 1: SELECCIÓN DE RESERVA
        # =========================================================
        frame_seleccion = tk.LabelFrame(self.modal, text=" 1. Seleccione Cliente ", font=("Arial", 14, "bold"), bg="#F3DCAB", fg="#333333")
        frame_seleccion.pack(fill="x", padx=20, pady=10, ipadx=5, ipady=5)

        self.combo_reservas_pago = ttk.Combobox(frame_seleccion, font=("Arial", 14), state="readonly", width=35)
        self.combo_reservas_pago.pack(pady=10)
        self.combo_reservas_pago.bind("<<ComboboxSelected>>", self.calcular_totales_liquidacion)

        self.cargar_reservas_modal()

        # =========================================================
        # ZONA 2: RESUMEN FINANCIERO (AUDITORÍA)
        # =========================================================
        frame_resumen = tk.LabelFrame(self.modal, text=" 2. Resumen de Cuenta ", font=("Arial", 14, "bold"), bg="#F3DCAB", fg="#333333")
        frame_resumen.pack(fill="x", padx=20, pady=10, ipadx=10, ipady=10)

        self.var_costo_cuarto = tk.StringVar(value="$0.00")
        self.var_costo_extras = tk.StringVar(value="$0.00")
        self.var_gran_total = tk.StringVar(value="$0.00")

        fila1 = tk.Frame(frame_resumen, bg="#F3DCAB")
        fila1.pack(fill="x", pady=2)
        tk.Label(fila1, text="Costo por Noches:", font=("Arial", 14), bg="#F3DCAB").pack(side="left")
        tk.Label(fila1, textvariable=self.var_costo_cuarto, font=("Arial", 14), bg="#F3DCAB").pack(side="right")

        fila2 = tk.Frame(frame_resumen, bg="#F3DCAB")
        fila2.pack(fill="x", pady=2)
        tk.Label(fila2, text="Cargos Extra (Bar/Servicios):", font=("Arial", 14), bg="#F3DCAB").pack(side="left")
        tk.Label(fila2, textvariable=self.var_costo_extras, font=("Arial", 14), bg="#F3DCAB").pack(side="right")

        tk.Frame(frame_resumen, height=2, bg="#333333").pack(fill="x", pady=10)

        fila3 = tk.Frame(frame_resumen, bg="#F3DCAB")
        fila3.pack(fill="x")
        tk.Label(fila3, text="TOTAL A PAGAR:", font=("Arial", 16, "bold"), bg="#F3DCAB", fg="#D32F2F").pack(side="left")
        tk.Label(fila3, textvariable=self.var_gran_total, font=("Arial", 18, "bold"), bg="#F3DCAB", fg="#D32F2F").pack(side="right")

        # =========================================================
        # ZONA 3: DATOS DEL PAGO
        # =========================================================
        frame_pago = tk.LabelFrame(self.modal, text=" 3. Método y Comprobante ", font=("Arial", 14, "bold"), bg="#F3DCAB", fg="#333333")
        frame_pago.pack(fill="x", padx=20, pady=10, ipadx=5, ipady=5)

        tk.Label(frame_pago, text="Método de Pago:", font=("Arial", 12), bg="#F3DCAB").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.combo_metodo = ttk.Combobox(frame_pago, font=("Arial", 12), state="readonly", values=["Efectivo", "Tarjeta Crédito", "Tarjeta Débito", "Transferencia"])
        self.combo_metodo.grid(row=0, column=1, padx=10, pady=10)
        self.combo_metodo.current(0)

        tk.Label(frame_pago, text="Comprobante:", font=("Arial", 12), bg="#F3DCAB").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.combo_comprobante = ttk.Combobox(frame_pago, font=("Arial", 12), state="readonly", values=["Boleta", "Factura"])
        self.combo_comprobante.grid(row=1, column=1, padx=10, pady=10)
        self.combo_comprobante.current(0)

        # =========================================================
        # BOTÓN FINAL
        # =========================================================
        self.btn_ejecutar_cobro = tk.Button(
            self.modal, text="✔️ Procesar Pago y Liberar Hab.", 
            font=("Arial", 16, "bold"), bg="#00838F", fg="white", 
            bd=3, relief="raised", pady=10,
            command=self.procesar_pago_final
        )
        self.btn_ejecutar_cobro.pack(fill="x", padx=20, pady=20)

    def cargar_reservas_modal(self):    
        self.ids_reservas_modal_memoria.clear()
        try:
            controller = ServicioController()
            bd_reservas = controller.obtener_todas_las_reservas_en_curso()

            if not bd_reservas:
                self.combo_reservas_pago['values'] = ["No hay habitaciones por cobrar"]
                self.combo_reservas_pago.current(0)
                return

            visual = []
            for fila in bd_reservas:
                self.ids_reservas_modal_memoria.append(fila[0]) 
                visual.append(f"Hab. {fila[1]} - {fila[2]} {fila[3]}")

            self.combo_reservas_pago['values'] = visual
            self.combo_reservas_pago.set("Seleccione una reserva...")

        except Exception as e:
            messagebox.showerror("Error", f"Fallo al cargar reservas: {e}")

    def calcular_totales_liquidacion(self, event=None):
        idx = self.combo_reservas_pago.current()
        if idx == -1 or not self.ids_reservas_modal_memoria or idx >= len(self.ids_reservas_modal_memoria):
            return

        try:
            id_reserva_real = self.ids_reservas_modal_memoria[idx]
            controller = CajaController()
            totales = controller.obtener_totales_liquidacion(id_reserva_real)
            
            if totales:
                if isinstance(totales, list):
                    fila = totales[0]
                else:
                    fila = totales
                
                costo_cuarto = float(fila[2])
                costo_extras = float(fila[3])
                gran_total = float(fila[4])
                
                # BLINDAJE: Guardamos el número en la RAM (Memoria lógica)
                # Esto es lo que va a la base de datos, NO lo que está en la pantalla.
                self.gran_total_memoria = gran_total
                
                self.var_costo_cuarto.set(f"${costo_cuarto:,.2f}")
                self.var_costo_extras.set(f"${costo_extras:,.2f}")
                self.var_gran_total.set(f"${gran_total:,.2f}")
                
        except Exception as e:
            messagebox.showerror("Error Matemático", str(e))

    def procesar_pago_final(self):
        idx = self.combo_reservas_pago.current()
        if idx == -1 or not self.ids_reservas_modal_memoria:
            messagebox.showwarning("Aviso", "Debe seleccionar un cliente antes de cobrar.")
            return

        try:
            id_reserva_real = self.ids_reservas_modal_memoria[idx]
            metodo = self.combo_metodo.get()
            comprobante = self.combo_comprobante.get()
            
            # BLINDAJE: Usamos la variable numérica pura, evitamos extraer de StringVars
            monto_total = getattr(self, 'gran_total_memoria', 0.0)

            if monto_total <= 0:
                raise ValueError("El monto total a pagar debe ser mayor a 0.00")

            confirmar = messagebox.askyesno(
                "Confirmar Transacción", 
                f"¿Proceder con el cobro de ${monto_total:,.2f} vía {metodo}?\nLa habitación será liberada."
            )
            
            if not confirmar:
                return

            # BLINDAJE: Extraemos el usuario sin importar si es dict o entero
            usr_actual = self.manager.usuario_actual
            if isinstance(usr_actual, dict):
                id_usuario_actual = int(usr_actual.get('id_usuario', usr_actual.get('id', 0)))
            else:
                id_usuario_actual = int(usr_actual) if usr_actual else 0

            if not id_usuario_actual:
                raise ValueError("Sesión inválida: No se detectó al usuario.")
            
            controller = CajaController()
            # Esta línea ya no congelará la BD porque corregimos el controlador
            controller.registrar_pago_completo(id_reserva_real, monto_total, metodo, comprobante, id_usuario_actual)

            messagebox.showinfo("Éxito", "Pago registrado y habitación liberada correctamente.")
            
            self.modal.destroy()      
            
            # Repinta la tabla (ahora sí funcionará porque SQL Server liberó la tabla)
            self.cargar_datos_pagos() 

        except ValueError as ve:
            messagebox.showwarning("Dato Inválido", str(ve))
        except Exception as e:
            messagebox.showerror("Error Transaccional", f"Fallo al registrar el pago:\n{e}")