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
from typing import Callable, Dict, List
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

class CustomerCard(ctk.CTkFrame):
    """Muestra un cliente, si puede comprar, y permite editarlo, eliminarlo o ver sus direcciones."""
    def __init__(self, master, customer: Dict, can_buy: bool, reason: str,
                 on_edit: Callable[[Dict], None],
                 on_delete: Callable[[int], None],
                 on_addresses: Callable[[int], None]):
        super().__init__(master, corner_radius=8, fg_color=COLORS["bg_card"])
        cid = customer["customer_id"]

        info = ctk.CTkFrame(self, fg_color="transparent")
        info.pack(side="left", padx=15, pady=10, fill="x", expand=True)
        full_name = f"{customer['name']} {customer.get('surname') or ''}".strip()
        ctk.CTkLabel(info, text=f"#{cid}  {full_name}", anchor="w",
                     font=ctk.CTkFont(size=14, weight="bold")).pack(fill="x")
        contact = (f"Email: {customer.get('email') or '-'}   |   Instagram: {customer.get('instagram') or '-'}"
                   f"   |   Tel: {customer.get('phone') or '-'}   |   Direcciones: {len(customer.get('addresses', []))}")
        ctk.CTkLabel(info, text=contact, anchor="w", font=ctk.CTkFont(size=12),
                     text_color=COLORS["muted_text"]).pack(fill="x")
        ctk.CTkLabel(info, text=reason, anchor="w", font=ctk.CTkFont(size=12, weight="bold"),
                     text_color=COLORS["status_ok"] if can_buy else COLORS["status_err"]).pack(fill="x")

        ctk.CTkButton(self, text="Eliminar", width=70, fg_color=COLORS["danger"],
                      hover_color=COLORS["danger_hover"],
                      command=lambda: on_delete(cid)).pack(side="right", padx=(5, 10), pady=8)
        ctk.CTkButton(self, text="Editar", width=70, fg_color=COLORS["info"],
                      hover_color=COLORS["info_hover"],
                      command=lambda: on_edit(customer)).pack(side="right", padx=5, pady=8)
        ctk.CTkButton(self, text="Direcciones", width=90, fg_color=COLORS["primary"],
                      hover_color=COLORS["primary_hover"],
                      command=lambda: on_addresses(cid)).pack(side="right", padx=5, pady=8)


class AddressCard(ctk.CTkFrame):
    """Muestra una dirección de delivery y permite editarla o eliminarla."""
    def __init__(self, master, address: Dict,
                 on_edit: Callable[[Dict], None],
                 on_delete: Callable[[int], None]):
        super().__init__(master, corner_radius=8, fg_color=COLORS["bg_card"])
        aid = address["address_id"]

        info = ctk.CTkFrame(self, fg_color="transparent")
        info.pack(side="left", padx=15, pady=10, fill="x", expand=True)
        ctk.CTkLabel(info, text=f"#{aid}  {address['address']}", anchor="w",
                     font=ctk.CTkFont(size=14, weight="bold")).pack(fill="x")
        place = ", ".join(x for x in (address.get("locality"), address.get("province"),
                                      address.get("country"), address.get("postal_code")) if x)
        detail = place + (f"   |   {address['notes']}" if address.get("notes") else "")
        if detail:
            ctk.CTkLabel(info, text=detail, anchor="w", font=ctk.CTkFont(size=12),
                         text_color=COLORS["muted_text"]).pack(fill="x")

        ctk.CTkButton(self, text="Eliminar", width=70, fg_color=COLORS["danger"],
                      hover_color=COLORS["danger_hover"],
                      command=lambda: on_delete(aid)).pack(side="right", padx=(5, 10), pady=8)
        ctk.CTkButton(self, text="Editar", width=70, fg_color=COLORS["info"],
                      hover_color=COLORS["info_hover"],
                      command=lambda: on_edit(address)).pack(side="right", padx=5, pady=8)

STATE_TEXT = {"pending": "Pendiente", "confirmed": "Confirmado", "cancelled": "Cancelado"}
STATE_COLOR = {"pending": COLORS["info"], "confirmed": COLORS["status_ok"], "cancelled": COLORS["status_err"]}


class OrderCard(ctk.CTkFrame):
    """
    Pedido con sus ítems. Los precios son una foto del momento de la compra.
    Solo si está pendiente se pueden quitar/agregar ítems, confirmar o cancelar.
    """
    def __init__(self, master, order: Dict, product_names: Dict[int, str], product_options: Dict[str, Dict],
                 on_confirm: Callable[[int], None],
                 on_cancel: Callable[[int], None],
                 on_add_item: Callable[[int, int, int], None],
                 on_remove_item: Callable[[int, int], None]):
        super().__init__(master, corner_radius=8, fg_color=COLORS["bg_card"])
        oid = order["order_id"]
        state = order["state"]
        pending = state == "pending"
        self.options = product_options
        self.on_add_item = on_add_item
        self.order_id = oid

        head = ctk.CTkFrame(self, fg_color="transparent")
        head.pack(fill="x", padx=15, pady=(10, 0))
        ctk.CTkLabel(head, text=f"Pedido #{oid}   |   {order['date']}", font=ctk.CTkFont(size=14, weight="bold")).pack(side="left")
        ctk.CTkLabel(head, text=f"{STATE_TEXT.get(state, state)}   |   Total: ${order['total']:,.2f}",
                     font=ctk.CTkFont(size=14, weight="bold"), text_color=STATE_COLOR.get(state)).pack(side="right")

        c = order["customer"]
        who = f"{c['name']} {c.get('surname') or ''}".strip()
        ctk.CTkLabel(self, text=f"Cliente: {who}   |   Email: {c.get('email') or '-'}   |   Tel: {c.get('phone') or '-'}",
                     anchor="w", font=ctk.CTkFont(size=12), text_color=COLORS["muted_text"]).pack(fill="x", padx=15)
        addresses = order.get("delivery_addresses") or []
        if addresses:
            text = "Entrega: " + "  /  ".join(
                ", ".join(x for x in (a["address"], a.get("locality"), a.get("province")) if x) for a in addresses)
            ctk.CTkLabel(self, text=text, anchor="w", justify="left", wraplength=560, font=ctk.CTkFont(size=12),
                         text_color=COLORS["muted_text"]).pack(fill="x", padx=15)
        if order.get("communication"):
            ctk.CTkLabel(self, text=f"Nota: {order['communication']}", anchor="w", font=ctk.CTkFont(size=12),
                         text_color=COLORS["muted_text"]).pack(fill="x", padx=15)

        items = order.get("items", [])
        for it in items:
            row = ctk.CTkFrame(self, fg_color="transparent")
            row.pack(fill="x", padx=15, pady=1)
            name = product_names.get(it["product_id"], f"Producto #{it['product_id']}")
            ctk.CTkLabel(row, anchor="w", font=ctk.CTkFont(size=13),
                         text=f"{it['quantity']} x {name}   @ ${it['unit_price']:,.2f}   =   ${it['subtotal']:,.2f}"
                         ).pack(side="left")
            if pending and len(items) > 1:    # el backend no deja un pedido vacío
                detail_id = it["order_detail_id"]
                ctk.CTkButton(row, text="Quitar", width=60, height=24, fg_color=COLORS["danger"],
                              hover_color=COLORS["danger_hover"],
                              command=lambda d=detail_id: on_remove_item(oid, d)).pack(side="right")

        if pending:
            add = ctk.CTkFrame(self, fg_color="transparent")
            add.pack(fill="x", padx=15, pady=(6, 0))
            labels = list(product_options) or ["(sin productos)"]
            self.menu_product = ctk.CTkOptionMenu(add, values=labels, height=26)
            self.menu_product.set(labels[0])
            self.menu_product.pack(side="left", fill="x", expand=True, padx=(0, 5))
            self.txt_qty = ctk.CTkEntry(add, width=50, height=26, placeholder_text="Cant.")
            self.txt_qty.pack(side="left", padx=(0, 5))
            ctk.CTkButton(add, text="Agregar ítem", width=90, height=26, command=self._add_item,
                          fg_color=COLORS["info"], hover_color=COLORS["info_hover"]).pack(side="left")

        buttons = ctk.CTkFrame(self, fg_color="transparent")
        buttons.pack(fill="x", padx=15, pady=10)
        if pending:
            ctk.CTkButton(buttons, text="Confirmar", width=90, fg_color=COLORS["success"],
                          hover_color=COLORS["success_hover"],
                          command=lambda: on_confirm(oid)).pack(side="right", padx=(5, 0))
            ctk.CTkButton(buttons, text="Cancelar", width=90, fg_color=COLORS["danger"],
                          hover_color=COLORS["danger_hover"],
                          command=lambda: on_cancel(oid)).pack(side="right")

    def _add_item(self):
        product = self.options.get(self.menu_product.get())
        qty = self.txt_qty.get().strip()
        if product and qty.isdigit() and int(qty) > 0:
            self.on_add_item(self.order_id, product["product_id"], int(qty))