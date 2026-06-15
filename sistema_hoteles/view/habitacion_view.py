import tkinter as tk
from tkinter import ttk
from tkinter import messagebox 

from controllers.habitacion_controller import HabitacionController

class HabitacionView:
    def __init__(self, root, manager):
        self.root = root
        self.manager = manager
        self.configurar_interfaz()
        
        # Metodo para llenar la pantalla con los valores de la BD
        self.refrescar_lista_habitaciones()

    def configurar_interfaz(self):

        # Div header
        self.frame_header = tk.Frame(self.root, background="#E0E0E0", bd=2, relief="groove")
        self.frame_header.pack(side=tk.TOP, fill="x")

        self.btn_volver = tk.Button(
            self.frame_header, text="⬅ Volver al Inicio", font=("Arial", 25, "bold"), 
            bg="#555555", fg="white", command=self.manager.mostrar_dashboard 
        )
        self.btn_volver.place(relx=0.02, rely=0.5, anchor="w")
        
        tk.Label(
            self.frame_header, text="HABITACIONES", background="#E0E0E0", 
            font=("Arial", 30, "bold"), fg="#333333"
        ).pack(pady=20)

        # Div main
        self.frame_main = tk.Frame(self.root, background="#F3DCAB")
        self.frame_main.pack(side=tk.TOP, fill="both", expand=True)

        self.frame_cuerpo = tk.Frame(self.frame_main, background="#F3DCAB")
        self.frame_cuerpo.pack(side=tk.TOP, fill="both", expand=True, padx=20, pady=10)

        # Listbox
        self.panel_izquierdo = tk.Frame(self.frame_cuerpo, background="#F3DCAB", width=250)
        self.panel_izquierdo.pack(side=tk.LEFT, fill="y", padx=(0, 20))
        self.panel_izquierdo.pack_propagate(False) 

        self.scroll_lista = tk.Scrollbar(self.panel_izquierdo, orient="vertical")
        self.scroll_lista.pack(side=tk.RIGHT, fill="y")

        self.lista_habitaciones = tk.Listbox(
            self.panel_izquierdo, font=("Arial", 14, "bold"), 
            bg="white", fg="#1565C0", bd=1, relief="solid",
            selectbackground="#1565C0", selectforeground="white",
            yscrollcommand=self.scroll_lista.set
        )
        self.lista_habitaciones.pack(side=tk.LEFT, fill="both", expand=True)
        self.scroll_lista.config(command=self.lista_habitaciones.yview)

        # Disparador: Detectar clic en la lista
        self.lista_habitaciones.bind("<<ListboxSelect>>", self.al_seleccionar_lista)

        self.panel_derecho = tk.Frame(self.frame_cuerpo, background="#F3DCAB")
        self.panel_derecho.pack(side=tk.LEFT, fill="both", expand=True)

        self.caja_tabla = tk.Frame(self.panel_derecho, background="#D9D9D9", bd=1, relief="solid")
        self.caja_tabla.pack(side=tk.TOP, fill="both", expand=True, pady=(0, 15))

        self.franja_botones = tk.Frame(self.panel_derecho, background="#E0E0E0", bd=1, relief="solid")
        self.franja_botones.pack(side=tk.TOP, fill="x") 
        
        self.sub_frame_botones = tk.Frame(self.franja_botones, background="#E0E0E0")
        self.sub_frame_botones.pack(pady=10)

        # Botones CRUD
        self.btn_agregar = tk.Button(
            self.sub_frame_botones, text="Agregar Habitación", font=("Arial", 18, "bold"), fg="#21DF96",
            command=self.abrir_formulario_agregar_habitacion
        )
        self.btn_agregar.pack(side=tk.LEFT, padx=10)

        self.btn_editar = tk.Button(
            self.sub_frame_botones, text="Editar Habitación", font=("Arial", 18, "bold"), fg="#1565C0",
            command=self.editar_habitacion
        )
        self.btn_editar.pack(side=tk.LEFT, padx=10)

        self.btn_eliminar = tk.Button(
            self.sub_frame_botones, text="Eliminar Habitación", font=("Arial", 18, "bold"), fg="#C62828",
            command=self.eliminar_habitacion
        )
        self.btn_eliminar.pack(side=tk.LEFT, padx=10)

        self.btn_gestionar_tipos = tk.Button(
            self.sub_frame_botones, text="Registrar Tipo", font=("Arial", 18, "bold"), fg="#EF6C00",
            command=self.abrir_formulario_tipos
        )
        self.btn_gestionar_tipos.pack(side=tk.LEFT, padx=(40, 10))

    def refrescar_lista_habitaciones(self):
        self.lista_habitaciones.delete(0, tk.END)
        self.ids_memoria = [] 
            
        controller = HabitacionController()
        habitaciones = controller.obtener_todas_las_habitaciones()
        
        if not habitaciones:
            self.lista_habitaciones.insert(tk.END, "Sin habitaciones")
            return

        for hab in habitaciones:
            id_hab = hab[0]
            num_hab = hab[1]
            
            self.ids_memoria.append(id_hab)
            self.lista_habitaciones.insert(tk.END, f"Habitación {num_hab}")

    def al_seleccionar_lista(self, event):

        seleccion = self.lista_habitaciones.curselection()

        if not seleccion: 
            return 
            
        indice = seleccion[0]
        
        if self.lista_habitaciones.get(indice) == "Sin habitaciones": return
            
        id_real = self.ids_memoria[indice]
        self.mostrar_detalle_habitacion(id_real)

    def mostrar_detalle_habitacion(self, id_habitacion):

        for widget in self.caja_tabla.winfo_children():
            widget.destroy()
            
        controller = HabitacionController()
        datos = controller.obtener_detalle_habitacion(id_habitacion) 
        
        if not datos: 
            return 
        
        num_hab, nombre_tipo, capacidad, precio, estado, piso = datos
        
        tk.Label(
            self.caja_tabla, text=f"Habitación {num_hab} - {nombre_tipo}", 
            bg="#D9D9D9", font=("Arial", 25, "bold"), fg="#333"
        ).pack(pady=20)
        
        self.frame_tarjetas = tk.Frame(self.caja_tabla, bg="#D9D9D9")
        self.frame_tarjetas.pack(pady=10)
        
        self.crear_tarjeta_info("Total de\nCamas", capacidad, 0, 0)
        self.crear_tarjeta_info("Precio\nActual", f"S/ {precio}", 0, 1)
        self.crear_tarjeta_info("Estado de\nDisponibilidad", estado, 0, 2)
        self.crear_tarjeta_info("Nivel del\nPiso", f"Piso {piso}", 1, 1)

    def crear_tarjeta_info(self, titulo, valor, fila, columna):

        self.tarjeta = tk.Frame(self.frame_tarjetas, bg="white", bd=1, relief="solid", width=250, height=200)
        self.tarjeta.grid(row=fila, column=columna, padx=15, pady=15)
        self.tarjeta.pack_propagate(False)
        
        tk.Label(self.tarjeta, text=titulo, bg="#00838F", fg="white", font=("Arial", 20, "bold"), pady=5).pack(fill="x")
        tk.Label(self.tarjeta, text=valor, bg="white", fg="#00838F", font=("Arial", 25, "bold")).pack(expand=True)

    def abrir_formulario_tipos(self):
        self.ventana_tipos = tk.Toplevel(self.root)
        self.ventana_tipos.title("Configurar Tipos de Habitación")
        self.ventana_tipos.geometry("500x600")
        self.ventana_tipos.resizable(False, False)
        self.ventana_tipos.configure(background="#F3DCAB")

        tk.Label(
            self.ventana_tipos, text="CREACION DE TIPOS", bg="#F3DCAB", 
            font=("Arial", 30, "bold"), pady=10
        ).pack(fill="x", side=tk.TOP, pady=(0, 20))

        tk.Label(self.ventana_tipos, text="Nombre:", bg="#F3DCAB", font=("Arial", 25, "bold")).pack(anchor="w", padx=40)
        self.tipo_hab_nombre = tk.Entry(self.ventana_tipos, font=("Arial", 22), bd=1, relief="solid")
        self.tipo_hab_nombre.pack(fill="x", padx=40, pady=(0, 15))

        tk.Label(self.ventana_tipos, text="Precio:", bg="#F3DCAB", font=("Arial", 25, "bold")).pack(anchor="w", padx=40)
        self.tipo_hab_precio = tk.Entry(self.ventana_tipos, font=("Arial", 22), bd=1, relief="solid")
        self.tipo_hab_precio.pack(fill="x", padx=40, pady=(0, 15))

        tk.Label(self.ventana_tipos, text="Capacidad de Personas:", bg="#F3DCAB", font=("Arial", 25, "bold")).pack(anchor="w", padx=40)
        self.tipo_hab_capacidad = tk.Spinbox(self.ventana_tipos, from_=1, to=10, font=("Arial", 22), bd=1, relief="solid")
        self.tipo_hab_capacidad.pack(fill="x", padx=40, pady=(0, 15))

        tk.Label(self.ventana_tipos, text="Descripción:", bg="#F3DCAB", font=("Arial", 25, "bold")).pack(anchor="w", padx=40)
        self.tipo_hab_descripcion = tk.Entry(self.ventana_tipos, font=("Arial", 22), bd=1, relief="solid")
        self.tipo_hab_descripcion.pack(fill="x", padx=40, pady=(0, 25))

        self.btn_guardar_tipo = tk.Button(
            self.ventana_tipos, text="Guardar Nuevo Tipo", bg="#ffffff", fg="#40e794", 
            font=("Arial", 20, "bold"), bd=2, relief="raised", command=self.ejecutar_formulario_tipo_habitacion
        )
        self.btn_guardar_tipo.pack(fill="x", padx=40)
        
        self.ventana_tipos.grab_set()

    def ejecutar_formulario_tipo_habitacion(self):
        nombre = self.tipo_hab_nombre.get().strip()
        precio = self.tipo_hab_precio.get().strip()
        capacidad = self.tipo_hab_capacidad.get().strip()
        descripcion = self.tipo_hab_descripcion.get().strip()

        if not nombre or not precio or not capacidad:
            messagebox.showwarning("Aviso", "Los campos Nombre, Precio y Capacidad no pueden quedar vacíos.")
            return

        controller = HabitacionController()

        try:
            controller.registrar_tipo_de_habitacion(nombre, precio, capacidad, descripcion)
            messagebox.showinfo("Exito", "Tipo de habitacion registrado corretamente")
            self.ventana_tipos.destroy()

        except ValueError as e:
            messagebox.showerror("Datos invalidados", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))
        
    def abrir_formulario_agregar_habitacion(self):
        self.ventana_agregar = tk.Toplevel(self.root)
        self.ventana_agregar.title("Agregar Nueva Habitación")
        self.ventana_agregar.geometry("500x500")
        self.ventana_agregar.resizable(False, False)
        self.ventana_agregar.configure(background="#F3DCAB")

        tk.Label(
            self.ventana_agregar, text="NUEVA HABITACION", bg="#F3DCAB", 
            font=("Arial", 30, "bold"), pady=10
        ).pack(fill="x", side=tk.TOP, pady=(0, 20))

        tk.Label(self.ventana_agregar, text="Numero de Piso:", bg="#F3DCAB", font=("Arial", 25, "bold")).pack(anchor="w", padx=40)
        self.num_piso = tk.Spinbox(self.ventana_agregar, from_=1, to=50, font=("Arial", 22), bd=2, relief="solid")
        self.num_piso.pack(fill="x", padx=40, pady=(0, 15))

        tk.Label(self.ventana_agregar, text="Numero de Habitacion:", bg="#F3DCAB", font=("Arial", 25, "bold")).pack(anchor="w", padx=40)
        self.num_habitacion = tk.Entry(self.ventana_agregar, font=("Arial", 22), bd=2, relief="solid")
        self.num_habitacion.pack(fill="x", padx=40, pady=(0, 15))

        tk.Label(self.ventana_agregar, text="Tipo de Habitacion:", bg="#F3DCAB", font=("Arial", 25, "bold")).pack(anchor="w", padx=40)
        self.tipo_habitacion = ttk.Combobox(self.ventana_agregar, font=("Arial", 22), state="readonly")
        self.tipo_habitacion.pack(fill="x", padx=40, pady=(0, 25))

        self.cargar_datos_combobox()

        self.btn_guardar_habitacion = tk.Button(
            self.ventana_agregar, text="Guardar Habitacion", bg="#40e794", fg="white", 
            font=("Arial", 22, "bold"), bd=2, relief="raised", command=self.ejecutar_registro_habitacion
        )
        self.btn_guardar_habitacion.pack(fill="x", padx=40)
        
        self.ventana_agregar.grab_set()

    def cargar_datos_combobox(self):
        controller = HabitacionController()
        self.datos_bd_tipos = controller.obtener_tipos_de_habitacion() 
        
        if not self.datos_bd_tipos:
            messagebox.showwarning("Aviso", "No hay tipos de habitación registrados. Cree uno primero.")
            self.tipo_habitacion['values'] = []
            return

        nombres_limpios = [fila[1] for fila in self.datos_bd_tipos]
        self.tipo_habitacion['values'] = nombres_limpios
        self.tipo_habitacion.current(0) 

    def ejecutar_registro_habitacion(self):

        piso = self.num_piso.get().strip()
        numero = self.num_habitacion.get().strip()
        indice_seleccionado = self.tipo_habitacion.current()
        
        if not piso or not numero:
            messagebox.showerror("Error", "Los campos Piso y Número son obligatorios")
            return

        if indice_seleccionado == -1: 
            messagebox.showerror("Error", "Debe seleccionar un Tipo de Habitación valido")
            return 
            
        id_tipo_sql = self.datos_bd_tipos[indice_seleccionado][0] 
        
        controller = HabitacionController()
        try:
            controller.registrar_habitacion(piso, numero, id_tipo_sql)
            messagebox.showinfo("Éxito", "Habitacion registrada correctamente en el sistema")
            
            self.ventana_agregar.destroy() 
            self.refrescar_lista_habitaciones()
            
        except ValueError as e:
            messagebox.showerror("Datos Inválidos", str(e))
        except Exception as e:
            messagebox.showerror("Error Crítico de BD", str(e))

    def eliminar_habitacion(self):
        
        seleccion = self.lista_habitaciones.curselection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona una habitación de la lista para eliminar.")
            return
        
        if self.lista_habitaciones.get(seleccion[0]) == "Sin habitaciones":
            return
        
        id_hab = self.ids_memoria[seleccion[0]]
        nombre_hab = self.lista_habitaciones.get(seleccion[0])
        
        confirmar = messagebox.askyesno(
            "Confirmar Eliminación", 
            f"¿Estás seguro de eliminar permanentemente la {nombre_hab}?"
        )
        
        if confirmar:
            try:
                controller = HabitacionController()
                controller.eliminar_habitacion(id_hab)
                
                messagebox.showinfo("Éxito", "Habitación eliminada correctamente.")
                self.refrescar_lista_habitaciones()
                
                for widget in self.caja_tabla.winfo_children():
                    widget.destroy()
                    
            except Exception as e:
                messagebox.showerror("Error Crítico", f"No se pudo eliminar: {e}")

    def editar_habitacion(self):

        seleccion = self.lista_habitaciones.curselection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona una habitación de la lista para editar.")
            return
        
        if self.lista_habitaciones.get(seleccion[0]) == "Sin habitaciones":
            return

        self.id_hab_edicion = self.ids_memoria[seleccion[0]]

        controller = HabitacionController()
        datos_actuales = controller.obtener_detalle_habitacion(self.id_hab_edicion)
        
        if not datos_actuales:
            messagebox.showerror("Error", "No se encontraron los datos de esta habitación.")
            return
            
        num_hab_actual = datos_actuales[0]
        nombre_tipo_actual = datos_actuales[1]
        piso_actual = datos_actuales[5]

        self.ventana_editar = tk.Toplevel(self.root)
        self.ventana_editar.title("Editar Habitación")
        self.ventana_editar.geometry("500x500")
        self.ventana_editar.resizable(False, False)
        self.ventana_editar.configure(background="#F3DCAB")

        tk.Label(
            self.ventana_editar, text="EDITAR HABITACIÓN", bg="#F3DCAB", 
            font=("Arial", 30, "bold"), pady=10
        ).pack(fill="x", side=tk.TOP, pady=(0, 20))

        # Piso 
        tk.Label(self.ventana_editar, text="Número de Piso:", bg="#F3DCAB", font=("Arial", 25, "bold")).pack(anchor="w", padx=40)
        self.var_piso_edicion = tk.StringVar(value=str(piso_actual))
        self.num_piso_edicion = tk.Spinbox(self.ventana_editar, from_=1, to=50, textvariable=self.var_piso_edicion, font=("Arial", 22), bd=2, relief="solid")
        self.num_piso_edicion.pack(fill="x", padx=40, pady=(0, 15))

        # Numero 
        tk.Label(self.ventana_editar, text="Número de Habitación:", bg="#F3DCAB", font=("Arial", 25, "bold")).pack(anchor="w", padx=40)
        self.num_habitacion_edicion = tk.Entry(self.ventana_editar, font=("Arial", 22), bd=2, relief="solid")
        self.num_habitacion_edicion.insert(0, str(num_hab_actual))
        self.num_habitacion_edicion.pack(fill="x", padx=40, pady=(0, 15))

        # Tipp habitacion
        tk.Label(self.ventana_editar, text="Tipo de Habitación:", bg="#F3DCAB", font=("Arial", 25, "bold")).pack(anchor="w", padx=40)
        self.tipo_habitacion_edicion = ttk.Combobox(self.ventana_editar, font=("Arial", 22), state="readonly")
        self.tipo_habitacion_edicion.pack(fill="x", padx=40, pady=(0, 25))

        # Cargar los tipos de habitacion desde la bd
        self.datos_bd_tipos_edicion = controller.obtener_tipos_de_habitacion()
        if self.datos_bd_tipos_edicion:
            nombres_limpios = [fila[1] for fila in self.datos_bd_tipos_edicion]
            self.tipo_habitacion_edicion['values'] = nombres_limpios
            
            if nombre_tipo_actual in nombres_limpios:
                indice_actual = nombres_limpios.index(nombre_tipo_actual)
                self.tipo_habitacion_edicion.current(indice_actual)
            else:
                self.tipo_habitacion_edicion.current(0)

        # Boton para realizar el update
        self.btn_actualizar_habitacion = tk.Button(
            self.ventana_editar, text="Actualizar Habitación", bg="#1565C0", fg="white", 
            font=("Arial", 22, "bold"), bd=2, relief="raised", command=self.ejecutar_edicion_habitacion
        )
        self.btn_actualizar_habitacion.pack(fill="x", padx=40)
        
        self.ventana_editar.grab_set()

    def ejecutar_edicion_habitacion(self):

        piso_nuevo = self.num_piso_edicion.get().strip()
        numero_nuevo = self.num_habitacion_edicion.get().strip()
        indice_seleccionado = self.tipo_habitacion_edicion.current()
        
        if not piso_nuevo or not numero_nuevo:
            messagebox.showerror("Error", "Los campos Piso y Número son obligatorios")
            return

        if indice_seleccionado == -1: 
            messagebox.showerror("Error", "Debe seleccionar un Tipo de Habitación válido")
            return 
            
        id_tipo_sql_nuevo = self.datos_bd_tipos_edicion[indice_seleccionado][0] 
        
        controller = HabitacionController()
        try:
            controller.actualizar_habitacion(self.id_hab_edicion, piso_nuevo, numero_nuevo, id_tipo_sql_nuevo)
            messagebox.showinfo("Éxito", "Habitación actualizada correctamente.")
            
            self.ventana_editar.destroy() 
            self.refrescar_lista_habitaciones()
            
            for widget in self.caja_tabla.winfo_children():
                widget.destroy()

            self.mostrar_detalle_habitacion(self.id_hab_edicion)
            
        except ValueError as e:
            messagebox.showerror("Datos Inválidos", str(e))
        except Exception as e:
            messagebox.showerror("Error Crítico de BD", str(e))