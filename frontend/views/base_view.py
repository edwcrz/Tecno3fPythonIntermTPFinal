"""
/frontend/views/base_view.py
Clase base de las tres pantallas (Productos, Clientes, Pedidos).
app.py llama a refresh() cada vez que se muestra la vista.
"""
import customtkinter as ctk


class BaseView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

    def refresh(self):
        """Se llama cada vez que la vista se muestra. Sobrescribir en cada vista."""
        pass