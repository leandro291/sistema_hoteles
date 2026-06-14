import tkinter as tk
from utils.utils import limpiar_ventana

from view.pago_view import PagoView
from view.login_view import LoginView
from view.cliente_view import ClienteView
from view.dashboard_view import DashboardView
from view.habitacion_view import HabitacionView
from view.asignacion_view import AsignacionView
from view.servicios_view import ServiciosView


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

    def mostrar_dashboard(self, datos_usuario=None):

        if datos_usuario is not None:
            self.usuario_actual = datos_usuario

        limpiar_ventana(self.root)
        self.vista_actual = DashboardView(self.root, manager=self)

    def mostrar_habitaciones(self):
        limpiar_ventana(self.root)
        self.vista_actual = HabitacionView(self.root, manager=self)

    def mostrar_asignaciones(self):
        limpiar_ventana(self.root)
        self.vista_actual = AsignacionView(self.root, manager=self)

    def mostrar_clientes(self):
        limpiar_ventana(self.root)
        self.vista_actual = ClienteView(self.root, manager=self)

    def mostrar_pagos(self):
        limpiar_ventana(self.root)
        self.vista_actual = PagoView(self.root, manager=self)
    
    def mostrar_servicios(self):
        limpiar_ventana(self.root)
        self.vista_actual = ServiciosView(self.root, manager=self)

if __name__ == "__main__":
    ventana  = tk.Tk()
    app = AppManager(ventana)
    ventana.mainloop()