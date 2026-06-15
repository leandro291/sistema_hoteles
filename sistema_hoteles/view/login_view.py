import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk

from controllers.auth_controller import AuthController

class LoginView:
    def __init__(self, root, manager):
        self.root = root
        self.manager = manager

        self.configurar_interfaz()

    def configurar_interfaz(self):

        carpeta_vistas = os.path.dirname(__file__)
        carpeta_raiz = os.path.dirname(carpeta_vistas)
        ruta_imagen = os.path.join(carpeta_raiz, 'assets', 'login', 'logo.webp')
        imagen_original = Image.open(ruta_imagen)
        imagen_redimensionada = imagen_original.resize((350, 350))
        
        self.image_tk = ImageTk.PhotoImage(imagen_redimensionada)
        self.div_izquierdo = tk.Frame(self.root, background="#E2E2E2")
        self.div_izquierdo.pack(side=tk.LEFT, fill="both", expand=True)
        self.div_izquierdo.pack_propagate(False)

        #Frame izquierda -> Para manejar la informacion personal
        tk.Label(self.div_izquierdo, image=self.image_tk).pack(pady=(80,70))
        tk.Label(self.div_izquierdo, text="Direccion: Av Canta Callao 123", background="#E2E2E2" , font=("Arial", 16, "bold")).pack(pady=2)
        tk.Label(self.div_izquierdo, text="Celular: +51 932 921 321", background="#E2E2E2" , font=("Arial", 16, "bold")).pack(pady=2)
        tk.Label(self.div_izquierdo, text="Email: gestion_hotel@unac.edu.pe", background="#E2E2E2" , font=("Arial", 16, "bold")).pack(pady=2)
        tk.Label(self.div_izquierdo, text="Callao (Bellavista) - Perú", background="#E2E2E2" , font=("Arial", 16, "bold")).pack(pady=2)
        tk.Label(self.div_izquierdo, text="Copyright © 2026 | Todos los derechos reservados ", background="#E2E2E2" ,font=("Arial", 18, "bold")).pack(pady=20)

        #Frame derecho -> Para manejar el inicio de sesion y registro del usuario
        self.div_derecho = tk.Frame(self.root, background="#F3DCAB")
        self.div_derecho.pack(side=tk.RIGHT, fill="both", expand=True)
        self.div_derecho.pack_propagate(False)

        self.login_usuario()

    def login_usuario(self):

        if hasattr(self, 'formulario'):
            self.formulario.destroy()

        #Subframe -> Para mantener el contenido alineado
        self.formulario = tk.Frame(self.div_derecho, background="#F3DCAB")
        self.formulario.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(self.formulario, text="Inicio de sesion", background="#F3DCAB", font=("Arial", 40, "bold")).pack(pady=(0, 40))

        tk.Label(self.formulario, text="Nombre de usuario", background="#F3DCAB", font=("Arial",25, "bold")).pack(anchor="w")
        self.inicio_usuario = tk.Entry(self.formulario, font=("Arial", 24))
        self.inicio_usuario.pack(ipady=3, pady=(5, 30), fill="x")

        tk.Label(self.formulario, text="Contraseña", background="#F3DCAB", font=("Arial",25, "bold")).pack(anchor="w")
        self.inicio_contrasena = tk.Entry(self.formulario, font=("Arial", 24), show="*") 
        self.inicio_contrasena.pack(ipady=3, pady=(5, 10), fill="x")

        self.var_mostrar_pwd = tk.BooleanVar()
        self.casilla_mostrar = tk.Checkbutton(
            self.formulario, text="Mostrar contraseña", background="#F3DCAB", 
            font=("Arial", 12), variable=self.var_mostrar_pwd, command=self.toggle_contrasena_login
        )
        self.casilla_mostrar.pack(anchor="w", pady=(0, 30))

        self.boton_iniciar = tk.Button(self.formulario, text="Iniciar", font=("Arial", 20, "bold"), bd=2, relief="raised", command=self.ejecutar_login)
        self.boton_iniciar.pack(pady=10, ipady=3, fill="x")

        self.boton_registrar = tk.Button(self.formulario, text="Registrar", font=("Arial", 20, "bold"), bd=2, relief="raised", command=self.registrar_usuario)
        self.boton_registrar.pack(pady=10, ipady=3, fill="x")

    def registrar_usuario(self):
        self.formulario.destroy()

        self.formulario = tk.Frame(self.div_derecho, background="#F3DCAB")
        self.formulario.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(self.formulario, text="Registrarse", background="#F3DCAB", font=("Arial", 40, "bold")).pack(pady=(0, 40))

        tk.Label(self.formulario, text="Nombre de usuario", background="#F3DCAB", font=("Arial",25, "bold")).pack(anchor="w")
        self.registro_usuario = tk.Entry(self.formulario, font=("Arial", 24))
        self.registro_usuario.pack(ipady=3, pady=(5, 20), fill="x")

        tk.Label(self.formulario, text="Contraseña", background="#F3DCAB", font=("Arial",25, "bold")).pack(anchor="w")
        self.registro_contrasena = tk.Entry(self.formulario, font=("Arial", 24), show="*") 
        self.registro_contrasena.pack(ipady=3, pady=(5, 20), fill="x")

        tk.Label(self.formulario, text="Rol", background="#F3DCAB", font=("Arial",25, "bold")).pack(anchor="w")
        self.registro_rol = ttk.Combobox(self.formulario, font=("Arial", 24), state="readonly")
        self.registro_rol['values'] = ["Recepcionista", "Administrador"]
        self.registro_rol.current(0)
        self.registro_rol.pack(ipady=3, pady=(5, 20), fill="x")

        self.boton_registrarse = tk.Button(self.formulario, text="Registrarse", font=("Arial", 20, "bold"), bd=2, relief="raised", command=self.ejecutar_registro)
        self.boton_registrarse.pack(pady=10, ipady=3, fill="x")

        self.boton_inicio = tk.Button(self.formulario, text="Regresar", font=("Arial", 20, "bold"), bd=2, relief="raised", command=self.login_usuario)
        self.boton_inicio.pack(pady=10, ipady=3, fill="x")

    def ejecutar_registro(self):

        nombre = self.registro_usuario.get().strip()
        contrasena = self.registro_contrasena.get() 
        rol = self.registro_rol.get()

        controlador = AuthController()

        try:

            controlador.registrar_nuevo_usuario(
                nombre, 
                contrasena, 
                rol
            )

            messagebox.showinfo("Exito", "Usuario registrado correctamente")
            self.login_usuario()

        except ValueError as e:
            messagebox.showerror("Datos invalidados", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def ejecutar_login(self):

        login_usuario = self.inicio_usuario.get().strip()
        login_contrasena = self.inicio_contrasena.get()

        controlador = AuthController()

        try:
            datos = controlador.iniciar_sesion(login_usuario, login_contrasena)
            self.manager.mostrar_dashboard(datos)

        except ValueError as e:
            messagebox.showerror("Datos invalidados", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def toggle_contrasena_login(self):
        
        if self.var_mostrar_pwd.get():
            self.inicio_contrasena.config(show="")
        else:
            self.inicio_contrasena.config(show="*")


if __name__ == "__main__":
    
    ventana = tk.Tk()
    aplicacion = LoginView(ventana)
    ventana.mainloop()