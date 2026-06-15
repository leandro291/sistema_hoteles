def limpiar_ventana(root):
    for widget in root.winfo_children():
        widget.destroy()