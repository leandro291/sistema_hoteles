import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from controllers.cliente_controller import ClienteController

class ClienteView:
    def __init__(self, root, manager):
        self.root = root
        self.manager = manager
        self.configurar_interfaz()
        self.recargar_tabla_clientes()

    def configurar_interfaz(self):

        # --- Cabecera principal ---
        self.frame_header = tk.Frame(self.root, background="#E0E0E0", bd=2, relief="groove")
        self.frame_header.pack(side=tk.TOP, fill="x")

        self.btn_volver = tk.Button(
            self.frame_header, text="⬅ Volver", font=("Arial", 16, "bold"), 
            bg="#555555", fg="white", command=self.manager.mostrar_dashboard 
        )
        self.btn_volver.place(relx=0.02, rely=0.5, anchor="w")
        
        tk.Label(
            self.frame_header, text="CLIENTES", background="#E0E0E0", 
            font=("Arial", 40, "bold"), fg="#333333"
        ).pack(pady=10)

        # --- Contenedor principal ---
        self.frame_main = tk.Frame(self.root, background="#F3DCAB")
        self.frame_main.pack(side=tk.TOP, fill="both", expand=True, padx=10, pady=10)

        self.panel_izquierdo = tk.LabelFrame(
            self.frame_main, text="Clientes", font=("Arial", 24, "bold"), 
            background="#F3DCAB", bd=1, relief="solid", width=430
        )
        self.panel_izquierdo.pack(side=tk.LEFT, fill="y", padx=(0, 10))
        self.panel_izquierdo.pack_propagate(False) 

        self.form_frame = tk.Frame(self.panel_izquierdo, background="#F3DCAB")
        self.form_frame.pack(pady=20, padx=10, fill="x")

        self.menu_clientes()

        self.panel_derecho = tk.Frame(self.frame_main, background="white", bd=2, relief="solid")
        self.panel_derecho.pack(side=tk.LEFT, fill="both", expand=True)

        self.menu_tablas()

    def menu_clientes(self):

        # Nombre
        tk.Label(self.form_frame, text="Nombre:", bg="#F3DCAB", font=("Arial", 18, "bold")).grid(row=0, column=0, sticky="w", pady=5)
        self.nombre = tk.Entry(self.form_frame, font=("Arial", 18), bd=1, relief="solid", width=20)
        self.nombre.grid(row=0, column=1, pady=5, padx=5)

        # Apellido
        tk.Label(self.form_frame, text="Apellido:", bg="#F3DCAB", font=("Arial", 18, "bold")).grid(row=1, column=0, sticky="w", pady=5)
        self.apellido = tk.Entry(self.form_frame, font=("Arial", 18), bd=1, relief="solid", width=20)
        self.apellido.grid(row=1, column=1, pady=5, padx=5)

        # Tipo de documento
        tk.Label(self.form_frame, text="Tipo doc:", bg="#F3DCAB", font=("Arial", 18, "bold")).grid(row=2, column=0, sticky="w", pady=5)
        self.tipo_documento = ttk.Combobox(self.form_frame, font=("Arial", 18), state="readonly", width=20)
        self.tipo_documento.grid(row=2, column=1, pady=5, padx=5)
        self.tipo_documento['values'] = ["DNI","Carnet Extranjería"]
        self.tipo_documento.current(0)

        # Dirección
        tk.Label(self.form_frame, text="Num doc:", bg="#F3DCAB", font=("Arial", 18, "bold")).grid(row=3, column=0, sticky="w", pady=5)
        self.numero_documento = tk.Entry(self.form_frame, font=("Arial", 18), bd=1, relief="solid", width=20)
        self.numero_documento.grid(row=3, column=1, pady=5, padx=5)

        # Telefono
        tk.Label(self.form_frame, text="Telefono:", bg="#F3DCAB", font=("Arial", 18, "bold")).grid(row=4, column=0, sticky="w", pady=5)
        self.telefono = tk.Entry(self.form_frame, font=("Arial", 18), bd=1, relief="solid", width=20)
        self.telefono.grid(row=4, column=1, pady=5, padx=5)

        # Correo
        tk.Label(self.form_frame, text="Correo:", bg="#F3DCAB", font=("Arial", 18, "bold")).grid(row=5, column=0, sticky="w", pady=5)
        self.correo = tk.Entry(self.form_frame, font=("Arial", 18), bd=1, relief="solid", width=20)
        self.correo.grid(row=5, column=1, pady=5, padx=5)

        # Direccion
        tk.Label(self.form_frame, text="Direccion:", bg="#F3DCAB", font=("Arial", 18, "bold")).grid(row=6, column=0, sticky="w", pady=5)
        self.direccion = tk.Entry(self.form_frame, font=("Arial", 18), bd=1, relief="solid", width=20)
        self.direccion.grid(row=6, column=1, pady=5, padx=5)

        self.btn_frame = tk.Frame(self.panel_izquierdo, background="#F3DCAB")
        self.btn_frame.pack(pady=20)

        self.btn_ingresar = tk.Button(
            self.btn_frame, text="Registrar", font=("Arial", 20, "bold"), bg="white",
            bd=2, relief="raised", command=self.registrar_cliente
        )
        self.btn_ingresar.grid(row=0, column=0, columnspan=2, pady=(0, 20), ipadx=20)

        self.btn_eliminar = tk.Button(
            self.btn_frame, text="Eliminar", font=("Arial", 20, "bold"), bg="white",
            bd=2, relief="raised", command=self.eliminar_cliente
        )
        self.btn_eliminar.grid(row=1, column=0, padx=10)

        self.btn_modificar = tk.Button(
            self.btn_frame, text="Modificar", font=("Arial", 20, "bold"), bg="white",
            bd=2, relief="raised", command=self.modificar_cliente
        )
        self.btn_modificar.grid(row=1, column=1, padx=10)

    def menu_tablas(self):

        # Configuración del estilo de la tabla
        estilo = ttk.Style()
        estilo.configure("Treeview.Heading", font=("Arial", 18, "bold"), background="#E0E0E0", foreground="#333")
        estilo.configure("Treeview", font=("Arial", 16), rowheight=25)

        # Barras de desplazamiento
        scroll_y = tk.Scrollbar(self.panel_derecho, orient="vertical")
        scroll_y.pack(side=tk.RIGHT, fill="y")
        
        scroll_x = tk.Scrollbar(self.panel_derecho, orient="horizontal")
        scroll_x.pack(side=tk.BOTTOM, fill="x")

        # Creación de la tabla
        columnas = ("ID", "Nombre", "Apellido", "Tipo doc", "Numero doc", "Telefono", "Correo", "Direccion")
        self.tabla_clientes = ttk.Treeview(
            self.panel_derecho, columns=columnas, show="headings", 
            yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set
        )
        self.tabla_clientes.pack(side=tk.LEFT, fill="both", expand=True)

        scroll_y.config(command=self.tabla_clientes.yview)
        scroll_x.config(command=self.tabla_clientes.xview)

        # Definición de cabeceras y anchos de columna
        self.tabla_clientes.heading("ID", text="ID")
        self.tabla_clientes.column("ID", width=50, anchor="center")
        
        self.tabla_clientes.heading("Nombre", text="Nombre")
        self.tabla_clientes.column("Nombre", width=200, anchor="w")
        
        self.tabla_clientes.heading("Apellido", text="Apellido")
        self.tabla_clientes.column("Apellido", width=200, anchor="center")
        
        self.tabla_clientes.heading("Tipo doc", text="Tipo doc")
        self.tabla_clientes.column("Tipo doc", width=200, anchor="center")
        
        self.tabla_clientes.heading("Numero doc", text="Numero doc")
        self.tabla_clientes.column("Numero doc", width=200, anchor="w")

        self.tabla_clientes.heading("Telefono", text="Telefono")
        self.tabla_clientes.column("Telefono", width=200, anchor="w")

        self.tabla_clientes.heading("Correo", text="Correo")
        self.tabla_clientes.column("Correo", width=200, anchor="w")

        self.tabla_clientes.heading("Direccion", text="Direccion")
        self.tabla_clientes.column("Direccion", width=200, anchor="w")

    def recargar_tabla_clientes(self):

        for item in self.tabla_clientes.get_children():
            self.tabla_clientes.delete(item)

        controller = ClienteController()
        lista_clientes = controller.obtener_todos_clientes()

        if not lista_clientes:
            return
        
        for cliente in lista_clientes:
            self.tabla_clientes.insert("", tk.END, values=cliente)


    def registrar_cliente(self):
        
        nombre = self.nombre.get().strip()
        apellido = self.apellido.get().strip()
        tipo_documento = self.tipo_documento.get().strip()
        numero_documento = self.numero_documento.get().strip()
        telefono = self.telefono.get().strip()
        correo = self.correo.get().strip()
        direccion = self.direccion.get().strip()

        if not nombre or not apellido or not numero_documento:
            messagebox.showwarning("Aviso", "Nombre, Apellido y Numero de Documento son obligatorios")
            return

        try:
            controller = ClienteController()
            controller.registrar_cliente(nombre, apellido, tipo_documento, numero_documento, 
                                        telefono, correo, direccion
                                        )
            messagebox.showinfo("Exito", "Cliente registrado correctamente en el sistema")

            self.recargar_tabla_clientes()

            self.nombre.delete(0, tk.END)
            self.apellido.delete(0, tk.END)
            self.tipo_documento.delete(0, tk.END)
            self.numero_documento.delete(0, tk.END)
            self.telefono.delete(0, tk.END)
            self.correo.delete(0, tk.END)
            self.direccion.delete(0, tk.END)

        except ValueError as e:
            messagebox.showerror("Datos Inválidos", str(e))
        except Exception as e:
            messagebox.showerror("Error Crítico de BD", str(e))


    def eliminar_cliente(self):
        seleccion = self.tabla_clientes.selection()

        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona un cliente de la tabla para eliminar.")
            return

        # Extraer los datos de la fila seleccionada
        item = self.tabla_clientes.item(seleccion[0])
        valores = item['values']
        id_cliente = valores[0]
        nombre_completo = f"{valores[1]} {valores[2]}"

        # Confirmacion para eliminar los datos
        confirmar = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Estás seguro de eliminar permanentemente a {nombre_completo}?"
        )

        if confirmar:
            try:
                controller = ClienteController()
                controller.eliminar_cliente(id_cliente)
                
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
                self.recargar_tabla_clientes()
            except Exception as e:
                messagebox.showerror("Error Crítico", f"No se pudo eliminar al cliente: {e}")


    def modificar_cliente(self):
        seleccion = self.tabla_clientes.selection()

        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona un cliente de la tabla para modificar")
            return

        # Extraemos los datos del Treeview para inyectarlos en el modal
        item = self.tabla_clientes.item(seleccion[0])
        valores = item['values']

        # Guardamos el ID en la instancia para usarlo al ejecutar el UPDATE
        self.id_cliente_edicion = valores[0]

        # Construcción del Modal de Edición
        self.ventana_editar = tk.Toplevel(self.root)
        self.ventana_editar.title("Modificar Cliente")
        self.ventana_editar.geometry("450x600")
        self.ventana_editar.resizable(False, False)
        self.ventana_editar.configure(background="#F3DCAB")
        self.ventana_editar.grab_set()

        tk.Label(
            self.ventana_editar, text="EDITAR CLIENTE", bg="#F3DCAB",
            font=("Arial", 24, "bold"), pady=10
        ).pack(fill="x")

        form_frame = tk.Frame(self.ventana_editar, bg="#F3DCAB")
        form_frame.pack(pady=10)

        # Nombre
        tk.Label(form_frame, text="Nombre:", bg="#F3DCAB", font=("Arial", 16, "bold")).grid(row=0, column=0, sticky="w", pady=5)
        self.edit_nombre = tk.Entry(form_frame, font=("Arial", 16), bd=1, relief="solid", width=20)
        self.edit_nombre.insert(0, valores[1])
        self.edit_nombre.grid(row=0, column=1, pady=5, padx=5)

        # Apellido
        tk.Label(form_frame, text="Apellido:", bg="#F3DCAB", font=("Arial", 16, "bold")).grid(row=1, column=0, sticky="w", pady=5)
        self.edit_apellido = tk.Entry(form_frame, font=("Arial", 16), bd=1, relief="solid", width=20)
        self.edit_apellido.insert(0, valores[2])
        self.edit_apellido.grid(row=1, column=1, pady=5, padx=5)

        # Tipo Documento
        tk.Label(form_frame, text="Tipo doc:", bg="#F3DCAB", font=("Arial", 16, "bold")).grid(row=2, column=0, sticky="w", pady=5)
        self.edit_tipo_doc = ttk.Combobox(form_frame, font=("Arial", 16), state="readonly", width=19)
        self.edit_tipo_doc['values'] = ["DNI", "Carnet Extranjería"]
        self.edit_tipo_doc.set(valores[3]) # Selecciona el actual
        self.edit_tipo_doc.grid(row=2, column=1, pady=5, padx=5)

        # Numero Documento
        tk.Label(form_frame, text="Num doc:", bg="#F3DCAB", font=("Arial", 16, "bold")).grid(row=3, column=0, sticky="w", pady=5)
        self.edit_num_doc = tk.Entry(form_frame, font=("Arial", 16), bd=1, relief="solid", width=20)
        self.edit_num_doc.insert(0, valores[4])
        self.edit_num_doc.grid(row=3, column=1, pady=5, padx=5)

        # Teléfono
        tk.Label(form_frame, text="Telefono:", bg="#F3DCAB", font=("Arial", 16, "bold")).grid(row=4, column=0, sticky="w", pady=5)
        self.edit_telefono = tk.Entry(form_frame, font=("Arial", 16), bd=1, relief="solid", width=20)
        self.edit_telefono.insert(0, valores[5]) 
        self.edit_telefono.grid(row=4, column=1, pady=5, padx=5)

        # Correo
        tk.Label(form_frame, text="Correo:", bg="#F3DCAB", font=("Arial", 16, "bold")).grid(row=5, column=0, sticky="w", pady=5)
        self.edit_correo = tk.Entry(form_frame, font=("Arial", 16), bd=1, relief="solid", width=20)
        self.edit_correo.insert(0, valores[6])
        self.edit_correo.grid(row=5, column=1, pady=5, padx=5)

        # Dirección
        tk.Label(form_frame, text="Direccion:", bg="#F3DCAB", font=("Arial", 16, "bold")).grid(row=6, column=0, sticky="w", pady=5)
        self.edit_direccion = tk.Entry(form_frame, font=("Arial", 16), bd=1, relief="solid", width=20)
        self.edit_direccion.insert(0, valores[7])
        self.edit_direccion.grid(row=6, column=1, pady=5, padx=5)

        # Botón de Guardar
        btn_guardar = tk.Button(
            self.ventana_editar, text="Guardar Cambios", font=("Arial", 18, "bold"),
            bg="#1565C0", fg="white", bd=2, relief="raised", command=self.ejecutar_modificacion_cliente
        )
        btn_guardar.pack(pady=20, fill="x", padx=50)


    def ejecutar_modificacion_cliente(self):

        nombre = self.edit_nombre.get().strip()
        apellido = self.edit_apellido.get().strip()
        tipo_doc = self.edit_tipo_doc.get().strip()
        num_doc = self.edit_num_doc.get().strip()
        telefono = self.edit_telefono.get().strip()
        correo = self.edit_correo.get().strip()
        direccion = self.edit_direccion.get().strip()

        if not nombre or not apellido or not num_doc:
            messagebox.showwarning("Aviso", "Nombre, Apellido y Numero de Documento no pueden quedar vacíos.")
            return

        try:
            controller = ClienteController()

            controller.actualizar_cliente(
                self.id_cliente_edicion,
                nombre, 
                apellido, 
                tipo_doc, 
                num_doc, 
                telefono, 
                correo, 
                direccion
            )

            messagebox.showinfo("Éxito", "Datos del cliente actualizados correctamente.")
            
            self.ventana_editar.destroy()
            self.recargar_tabla_clientes()
            
        except ValueError as e:
            messagebox.showerror("Datos Inválidos", str(e))
        except Exception as e:
            messagebox.showerror("Error Crítico de BD", str(e))