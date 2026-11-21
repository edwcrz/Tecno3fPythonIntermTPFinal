"""
notas en clase
cards es para hacer algunas muestras
a futuro se pueden agregar imagenes del producto
info del producto
permite borrar o editar el producto
"""

"""
Componente modular reutilizable diseñado para presentar la información individual de un producto (nombre, precio, stock) y 
proporcionar botones rápidos de acción para edición y eliminación.
"""
import customtkinter as ctk
from typing import Callable, Dict
from frontend.config import COLORS

class ProductCard(ctk.CTkFrame):
    def __init__(
        self,
        master,
        product: Dict,
        on_edit: Callable[[Dict], None],
        on_delete: Callable[[int], None]
    ):
        super().__init__(master, corner_radius=8, fg_color=COLORS["bg_card"])
        self.product = product

        info_text = f"#{product['id']}  {product['name']}   |   ${product['price']:.2f}   |   Stock: {product['stock']}"
        self.label = ctk.CTkLabel(self, text=info_text, anchor="w", font=ctk.CTkFont(size=14))
        self.label.pack(side="left", padx=15, pady=10, fill="x", expand=True)

        self.btn_delete = ctk.CTkButton(
            self,
            text="Eliminar",
            width=70,
            fg_color=COLORS["danger"],
            hover_color=COLORS["danger_hover"],
            command=lambda: on_delete(product["id"])
        )
        self.btn_delete.pack(side="right", padx=(5, 10), pady=8)

        self.btn_edit = ctk.CTkButton(
            self,
            text="Editar",
            width=70,
            fg_color=COLORS["info"],
            hover_color=COLORS["info_hover"],
            command=lambda: on_edit(product)
        )
        self.btn_edit.pack(side="right", padx=5, pady=8)