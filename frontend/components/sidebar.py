"""
/frontend/components/sidebar.py
Menú lateral con los botones de navegación entre módulos
(Productos, Clientes, Pedidos) y resaltado visual del botón activo.
"""
import customtkinter as ctk
from typing import Callable

from frontend.config import COLORS


class AppSidebar(ctk.CTkFrame):
    TEXT_DEFAULT = ("gray10", "gray90")
    HOVER_DEFAULT = ("gray70", "gray30")

    def __init__(self, master, on_navigate: Callable[[str], None]):
        super().__init__(master, width=200, corner_radius=0)
        self.pack_propagate(False)  # mantiene el ancho fijo de 200 px
        self.on_navigate = on_navigate
        self.buttons: dict[str, ctk.CTkButton] = {}

        title_label = ctk.CTkLabel(
            self,
            text="Menú",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        title_label.pack(padx=20, pady=(20, 10))

        nav_items = [
            ("Productos", "product"),
            ("Clientes", "customer"),
            ("Pedidos", "order"),
        ]
        for text, key in nav_items:
            btn = ctk.CTkButton(
                self,
                text=text,
                fg_color="transparent",
                text_color=self.TEXT_DEFAULT,
                hover_color=self.HOVER_DEFAULT,
                anchor="w",
                command=lambda k=key: self.on_navigate(k),
            )
            btn.pack(fill="x", padx=10, pady=5)
            self.buttons[key] = btn

    def set_active_button(self, view_name: str):
        for key, btn in self.buttons.items():
            if key == view_name:
                btn.configure(
                    fg_color=COLORS["primary"],
                    hover_color=COLORS["primary_hover"],
                    text_color="white",
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    hover_color=self.HOVER_DEFAULT,
                    text_color=self.TEXT_DEFAULT,
                )