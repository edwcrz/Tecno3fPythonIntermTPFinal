"""
/frontend/app.py

Contenedor principal de la interfaz de usuario.
Organiza el sidebar de navegación a la izquierda y la zona de contenido
dinámico a la derecha, e intercambia las vistas (Productos, Clientes, Ventas).
"""

import customtkinter as ctk

from frontend.config import (
    WINDOW_TITLE, WINDOW_SIZE, MIN_WINDOW_SIZE, THEME_MODE, COLOR_THEME
)
from frontend.components.sidebar import AppSidebar
from frontend.views.product_view import ProductView
from frontend.views.customer_view import CustomerView
from frontend.views.order_view import OrderView

ctk.set_appearance_mode(THEME_MODE)
ctk.set_default_color_theme(COLOR_THEME)


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(WINDOW_TITLE)
        self.geometry(WINDOW_SIZE)
        self.minsize(*MIN_WINDOW_SIZE)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = AppSidebar(self, on_navigate=self.show_view)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.content_area = ctk.CTkFrame(self)
        self.content_area.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.views = {
            "product": ProductView(self.content_area),
            # "customer": CustomerView(self.content_area),
            # "order": OrderView(self.content_area),
        }
        self.show_view("product")

    def show_view(self, view_name: str):
        selected_view = self.views.get(view_name)
        if selected_view is None:
            return

        for view in self.views.values():
            view.pack_forget()

        self.sidebar.set_active_button(view_name)
        selected_view.pack(fill="both", expand=True)
        selected_view.refresh()