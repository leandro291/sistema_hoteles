import tkinter as tk
from utils.utils import limpiar_ventana

from view.dashboard_view import DashboardView
from view.login_view import LoginView


class AppManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de gestion de hoteles")
        self.root.geometry("1400x800")
        self.root.resizable(False, False)

        self.usuario_actual = None

        self.mostrar_login()

    def mostrar_login(self):
        limpiar_ventana(self.root)
        self.vista_actual = LoginView(self.root, manager=self)

    def mostrar_dashboard(self, datos_usuario):
        self.usuario_actual = datos_usuario
        limpiar_ventana(self.root)
        self.vista_actual = DashboardView(self.root, manager=self)

if __name__ == "__main__":
    ventana  = tk.Tk()
    app = AppManager(ventana)
    ventana.mainloop()