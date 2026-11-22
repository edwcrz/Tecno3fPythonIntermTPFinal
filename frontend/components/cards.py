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
        on_delete: Callable[[int], None],
        on_restock: Callable[[int, int], None]):   # (product_id, cantidad a reponer)

        super().__init__(master, corner_radius=8, fg_color=COLORS["bg_card"])
        self.product = product
        pid = product["product_id"]

        # Columna izquierda: dos líneas de información
        info = ctk.CTkFrame(self, fg_color="transparent")
        info.pack(side="left", padx=15, pady=10, fill="x", expand=True)

        title = f"#{pid}  {product['name']}  ({product['size']})   |   {product['product_category']}"
        ctk.CTkLabel(info, text=title, anchor="w", font=ctk.CTkFont(size=14, weight="bold")).pack(fill="x")

        base = product.get("base_price")
        price_text = f"${base:,.2f}" if base is not None else "Sin precio base (no se puede vender)"
        stock_text = (f"Stock: {product['stock']}   |   Reservado: {product['reserved_stock']}   |   "
                      f"Disponible: {product['available']}   |   Precio base: {price_text}")
        no_sale = base is None or product["available"] <= 0
        ctk.CTkLabel(info, text=stock_text, anchor="w", font=ctk.CTkFont(size=12),
                     text_color=COLORS["status_err"] if no_sale else COLORS["muted_text"]).pack(fill="x")

        # Columna derecha: botones
        self.btn_delete = ctk.CTkButton(
            self,
            text="Eliminar",
            width=70,
            fg_color=COLORS["danger"],
            hover_color=COLORS["danger_hover"],
            command=lambda: on_delete(pid)
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

        # Reposición de stock físico (producción o ingreso)
        self._on_restock = on_restock
        self.btn_restock = ctk.CTkButton(
            self,
            text="+ Stock",
            width=70,
            fg_color=COLORS["success"],
            hover_color=COLORS["success_hover"],
            command=self._restock
        )
        self.btn_restock.pack(side="right", padx=5, pady=8)

        self.txt_qty = ctk.CTkEntry(self, width=50, placeholder_text="Cant.")
        self.txt_qty.pack(side="right", padx=(5, 0), pady=8)

    def _restock(self):
        try:
            qty = int(self.txt_qty.get().strip())
        except ValueError:
            return
        if qty > 0:
            self._on_restock(self.product["product_id"], qty)


class PaymentMethodCard(ctk.CTkFrame):
    """Muestra un método de pago con su recargo en % y permite editarlo o eliminarlo."""
    def __init__(self, master, method: Dict,
                 on_edit: Callable[[Dict], None],
                 on_delete: Callable[[int], None]):
        super().__init__(master, corner_radius=8, fg_color=COLORS["bg_card"])
        mid = method["payment_method_id"]

        text = (f"#{mid}  {method['method_name']}   |   Recargo: {method['overload'] * 100:g}%   |   "
                f"Plazo: {method['payment_term']} días")
        ctk.CTkLabel(self, text=text, anchor="w", font=ctk.CTkFont(size=14)).pack(
            side="left", padx=15, pady=10, fill="x", expand=True)

        ctk.CTkButton(self, text="Eliminar", width=70, fg_color=COLORS["danger"],
                      hover_color=COLORS["danger_hover"],
                      command=lambda: on_delete(mid)).pack(side="right", padx=(5, 10), pady=8)
        ctk.CTkButton(self, text="Editar", width=70, fg_color=COLORS["info"],
                      hover_color=COLORS["info_hover"],
                      command=lambda: on_edit(method)).pack(side="right", padx=5, pady=8)