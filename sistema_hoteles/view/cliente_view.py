import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from controllers.cliente_controller import ClienteController

class ClienteView:
    def __init__(self, root, manager):
        self.root = root
        self.manager = manager
        self.configurar_interfaz()

    def configurar_interfaz(self):
        # --- HEADER ---
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

        # --- CONTENEDOR PRINCIPAL ---
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
        estilo.theme_use("default")
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

    def registrar_cliente(self):
        
        nombre = self.nombre.get()
        apellido = self.apellido.get()
        tipo_documento = self.tipo_documento.get()
        numero_documento = self.numero_documento.get()
        telefono = self.telefono.get()
        correo = self.correo.get()
        direccion = self.direccion.get()

        try:
            controller = ClienteController()
            controller.registrar_usuario(nombre, apellido, tipo_documento, numero_documento, 
                                        telefono, correo, direccion
                                        )
            messagebox.showinfo("Exito", "Cliente registrado correctamente en el sistema")
        except ValueError as e:
            messagebox.showerror("Datos Inválidos", str(e))
        except Exception as e:
            messagebox.showerror("Error Crítico de BD", str(e))


    def eliminar_cliente(self):
        pass

    def modificar_cliente(self):
        pass