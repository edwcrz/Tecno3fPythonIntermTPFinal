""""
formatos
formatos validos
validaciones solicitadas
guardar cambios
modificaciones de productos
formulario principal para cargar datos del producto
"""

"""
/frontend/components/forms.py
Formulario interactivo para creación y edición de productos. 
Realiza validaciones locales de datos numéricos y conmuta su interfaz entre los modos de inserción y actualización.
"""

import customtkinter as ctk
from typing import Callable, Optional, Dict
from frontend.config import COLORS

class ProductForm(ctk.CTkFrame):
    def __init__(self, master, on_save: Callable[[Optional[int], str, float, int], None]):
        super().__init__(master, corner_radius=10)
        self.on_save = on_save
        self.current_editing_id: Optional[int] = None

        self.title_lbl = ctk.CTkLabel(self, text="Datos del Producto", font=ctk.CTkFont(size=18, weight="bold"))
        self.title_lbl.pack(padx=20, pady=(20, 15))

        self.txt_name = ctk.CTkEntry(self, placeholder_text="Nombre del producto")
        self.txt_name.pack(padx=20, pady=8, fill="x")

        self.txt_price = ctk.CTkEntry(self, placeholder_text="Precio (ej: 1500.00)")
        self.txt_price.pack(padx=20, pady=8, fill="x")

        self.txt_stock = ctk.CTkEntry(self, placeholder_text="Stock disponible")
        self.txt_stock.pack(padx=20, pady=8, fill="x")

        self.btn_save = ctk.CTkButton(
            self,
            text="Agregar Producto",
            command=self._handle_save,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"]
        )
        self.btn_save.pack(padx=20, pady=(15, 5), fill="x")

        self.btn_cancel = ctk.CTkButton(
            self,
            text="Cancelar Edición",
            command=self.clear,
            fg_color=COLORS["cancel"],
            hover_color=COLORS["cancel_hover"]
        )

        self.status_lbl = ctk.CTkLabel(self, text="", text_color=COLORS["status_ok"])
        self.status_lbl.pack(padx=20, pady=12)

    def _handle_save(self):
        name = self.txt_name.get().strip()
        price_raw = self.txt_price.get().strip()
        stock_raw = self.txt_stock.get().strip()

        if not name or not price_raw or not stock_raw:
            self.set_status("Todos los campos son obligatorios.", is_error=True)
            return

        try:
            price = float(price_raw)
            stock = int(stock_raw)
        except ValueError:
            self.set_status("Precio o Stock con formato inválido.", is_error=True)
            return

        self.on_save(self.current_editing_id, name, price, stock)

    def populate(self, product: Dict):
        self.current_editing_id = product["id"]
        self.txt_name.delete(0, "end")
        self.txt_name.insert(0, product["name"])

        self.txt_price.delete(0, "end")
        self.txt_price.insert(0, str(product["price"]))

        self.txt_stock.delete(0, "end")
        self.txt_stock.insert(0, str(product["stock"]))

        self.btn_save.configure(text="Guardar Cambios", fg_color=COLORS["success"])
        self.btn_cancel.pack(padx=20, pady=(5, 0), fill="x")
        self.set_status(f"Modificando producto #{product['id']}")

    def clear(self):
        self.current_editing_id = None
        self.txt_name.delete(0, "end")
        self.txt_price.delete(0, "end")
        self.txt_stock.delete(0, "end")
        self.btn_save.configure(text="Agregar Producto", fg_color=COLORS["primary"])
        self.btn_cancel.pack_forget()

    def set_status(self, text: str, is_error: bool = False):
        self.status_lbl.configure(
            text=text,
            text_color=COLORS["status_err"] if is_error else COLORS["status_ok"]
        )