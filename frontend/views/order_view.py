"""
/frontend/views/order_view.py
Pantalla PEDIDOS. Agrupa dos tablas del backend en dos pestañas:
- Nuevo pedido: orders + order_detail (cliente, método de pago y varios productos)
- Pedidos: lista con estado, total, ítems y dirección de entrega (leída del cliente)
Sin stock disponible no se vende; el cliente necesita email y dirección.
"""

from typing import Dict, List, Optional
from tkinter import messagebox

import customtkinter as ctk

from frontend.services.order_service import OrderService
from frontend.services.customer_service import CustomerService
from frontend.services.product_service import ProductService
from frontend.components.forms import OrderForm, product_label
from frontend.components.cards import OrderCard
from frontend.views.base_view import BaseView
from frontend.config import COLORS


class OrderView(BaseView):
    def __init__(self, master):
        super().__init__(master)
        self.products: List[Dict] = []

        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=10, pady=(10, 0))
        ctk.CTkLabel(top, text="Pedidos", font=ctk.CTkFont(size=20, weight="bold")).pack(side="left")
        ctk.CTkButton(top, text="Actualizar", width=90, command=self.refresh).pack(side="right")

        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(fill="both", expand=True, padx=5, pady=5)
        self._build_new_tab(self.tabs.add("Nuevo pedido"))
        self._build_list_tab(self.tabs.add("Pedidos"))
        # La carga de datos la dispara refresh() cuando se muestra la vista.

    # ------------------------------------------------------------------ armado
    def _build_new_tab(self, tab):
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(0, weight=1)
        self.form = OrderForm(tab, on_save=self.handle_create)
        self.form.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    def _build_list_tab(self, tab):
        self.list_status = ctk.CTkLabel(tab, text="", text_color=COLORS["status_ok"], anchor="w", wraplength=700)
        self.list_status.pack(fill="x", padx=15, pady=(10, 0))
        self.order_list = ctk.CTkScrollableFrame(tab)
        self.order_list.pack(fill="both", expand=True, padx=10, pady=10)

    # ------------------------------------------------------------------ carga
    def refresh(self):
        """Se llama cada vez que la vista se muestra: recarga clientes, catálogo y pedidos."""
        customers, err = CustomerService.list_customers()
        if err:
            self.form.set_status(err, is_error=True)
            return
        catalog, err = ProductService.load_catalog()
        if err:
            self.form.set_status(err, is_error=True)
            return
        orders, err = OrderService.list_orders()
        if err:
            self.form.set_status(err, is_error=True)
            return

        # self.products = catalog["products"]
        # can_buy = [c for c in customers if CustomerService.sale_status(c)[0]]
        # sellable = [p for p in self.products if p["base_price"] is not None and p["available"] > 0]
        # self.form.set_options(can_buy, sellable, catalog["methods"])
        # self._render_orders(orders)
        self.products = catalog["products"]
        self.form.set_options(catalog["methods"])
        self._render_orders(orders)

    def _render_orders(self, orders: List[Dict]):
        for widget in self.order_list.winfo_children():
            widget.destroy()
        if not orders:
            ctk.CTkLabel(self.order_list, text="No hay pedidos registrados.", text_color=COLORS["muted_text"]).pack(pady=20)
            return
        names = {p["product_id"]: f"{p['name']} ({p['size']})" for p in self.products}
        options = {product_label(p): p for p in self.products
                   if p["base_price"] is not None and p["available"] > 0}
        for order in orders:
            card = OrderCard(self.order_list, order=order, product_names=names, product_options=options, on_confirm=self.handle_confirm, on_cancel=self.handle_cancel, on_add_item=self.handle_add_item, on_remove_item=self.handle_remove_item)
            card.pack(fill="x", padx=5, pady=5)

    def _list_status(self, text: str, is_error: bool = False):
        self.list_status.configure(text=text, text_color=COLORS["status_err"] if is_error else COLORS["status_ok"])

    # ------------------------------------------------------------------ pedidos
    def handle_create(self, customer_id: int, method_id: int, communication: Optional[str], items: List[Dict]):
        order, err = OrderService.create_order(customer_id, method_id, communication, items)
        if err:   # por ejemplo: "Stock insuficiente de 'Lemon pie': pedido 5, disponible 3"
            self.form.set_status(err, is_error=True)
            return
        self.form.clear()
        self.refresh()
        self.form.set_status(f"Pedido #{order['order_id']} creado. Total: ${order['total']:,.2f}")
        self._list_status(f"Pedido #{order['order_id']} creado.")

    def handle_confirm(self, order_id: int):
        if not messagebox.askyesno("Confirmar", f"¿Confirmar el pedido #{order_id}? Descuenta el stock.", parent=self):
            return
        self._change_state(order_id, "confirmed", "confirmado")

    def handle_cancel(self, order_id: int):
        if not messagebox.askyesno("Confirmar", f"¿Cancelar el pedido #{order_id}? Libera las reservas.", parent=self):
            return
        self._change_state(order_id, "cancelled", "cancelado")

    def _change_state(self, order_id: int, state: str, done: str):
        _, err = OrderService.change_state(order_id, state)
        if err:
            self._list_status(err, is_error=True)
            return
        self.refresh()
        self._list_status(f"Pedido #{order_id} {done}.")

    def handle_add_item(self, order_id: int, product_id: int, quantity: int):
        _, err = OrderService.add_item(order_id, product_id, quantity)
        if err:
            self._list_status(err, is_error=True)
            return
        self.refresh()
        self._list_status(f"Ítem agregado al pedido #{order_id}.")

    def handle_remove_item(self, order_id: int, order_detail_id: int):
        _, err = OrderService.remove_item(order_id, order_detail_id)
        if err:
            self._list_status(err, is_error=True)
            return
        self.refresh()
        self._list_status(f"Ítem quitado del pedido #{order_id}.")