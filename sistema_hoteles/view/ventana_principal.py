import os
import tkinter as tk
from PIL import Image, ImageTk

class VentanaPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de gestion de hoteles")
        self.root.geometry("1400x800")
        self.root.resizable(False, False)

        self.configurar_interfaz()

    def configurar_interfaz(self):

        carpeta_actual = os.path.dirname(__file__)
        ruta_imagen = os.path.join(carpeta_actual, 'logo.webp')
        imagen_original = Image.open(ruta_imagen)
        imagen_redimensionada = imagen_original.resize((350, 350))
        self.image_tk = ImageTk.PhotoImage(imagen_redimensionada)
        self.div_izquierdo = tk.Frame(self.root, background="#E2E2E2")
        self.div_izquierdo.pack(side=tk.LEFT, fill="both", expand=True)
        self.div_izquierdo.pack_propagate(False)

        tk.Label(self.div_izquierdo, image=self.image_tk).pack(pady=(50,40))
        tk.Label(self.div_izquierdo, text="Direccion: Av Canta Callao 123", background="#E2E2E2" ,font=("Arial", 16, "bold")).pack(pady=2)
        tk.Label(self.div_izquierdo, text="Celular: +51 932 921 321", background="#E2E2E2" ,font=("Arial", 16, "bold")).pack(pady=2)
        tk.Label(self.div_izquierdo, text="Email: gestion_hotel@unac.edu.pe", background="#E2E2E2" ,font=("Arial", 16, "bold")).pack(pady=2)
        tk.Label(self.div_izquierdo, text="Callao (Bellavista) - Perú", background="#E2E2E2" ,font=("Arial", 16, "bold")).pack(pady=2)
        tk.Label(self.div_izquierdo, text="Copyright © 2026 | Todos los derechos reservados ", background="#E2E2E2" ,font=("Arial", 18, "bold")).pack(pady=20)

        self.div_derecho = tk.Frame(self.root, background="#F3DCAB")
        self.div_derecho.pack(side=tk.RIGHT, fill="both", expand=True)
        self.div_derecho.pack_propagate(False)



if __name__ == "__main__":
    
    ventana = tk.Tk()
    aplicacion = VentanaPrincipal(ventana)

    ventana.mainloop()