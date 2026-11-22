"""
/frontend/views/product_view.py
anotaciones en clase
que es lo que el usuario ve
no lo que va a mandar

va el pannel del formulario
el pannel del listado
cargar los datos para actualizar con load data
para cambiar de pantalla, se refrezque con el cambio anterior
para confirmar el delete
refresh del load data
"""

"""
Pantalla PRODUCTOS. Agrupa tres tablas del backend en tres pestañas:
- Catálogo: product (formulario + tarjetas con stock, reservado, disponible y precio base)
- Métodos de pago: payment_method (formulario + tarjetas con su recargo en %)
- Precios: product_payment (precio base) y precio final por método de pago
"""

from typing import Dict, Optional
from tkinter import messagebox

import customtkinter as ctk

from frontend.services.product_service import ProductService
from frontend.components.forms import ProductForm, PaymentMethodForm, PriceForm
from frontend.components.cards import ProductCard, PaymentMethodCard
from frontend.views.base_view import BaseView
from frontend.config import COLORS


class ProductView(BaseView):
    def __init__(self, master):
        super().__init__(master)
        self.catalog: Dict = {"products": [], "methods": []}

        # Barra superior: título y botón de actualizar (recarga las tres pestañas)
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=10, pady=(10, 0))
        ctk.CTkLabel(top, text="Productos", font=ctk.CTkFont(size=20, weight="bold")).pack(side="left")
        ctk.CTkButton(top, text="Actualizar", width=90, command=self.refresh).pack(side="right")

        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(fill="both", expand=True, padx=5, pady=5)
        self._build_catalog_tab(self.tabs.add("Catálogo"))
        self._build_methods_tab(self.tabs.add("Métodos de pago"))
        self._build_prices_tab(self.tabs.add("Precios"))
        # La carga de datos la dispara refresh() cuando se muestra la vista.

    # ------------------------------------------------------------------ armado
    def _two_columns(self, tab):
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_columnconfigure(1, weight=2)
        tab.grid_rowconfigure(0, weight=1)

    def _list_panel(self, tab, title: str) -> ctk.CTkScrollableFrame:
        container = ctk.CTkFrame(tab, corner_radius=10)
        container.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="nsew")
        ctk.CTkLabel(container, text=title, font=ctk.CTkFont(size=18, weight="bold")).pack(
            anchor="w", padx=15, pady=15)
        scroll = ctk.CTkScrollableFrame(container)
        scroll.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        return scroll

    def _build_catalog_tab(self, tab):
        self._two_columns(tab)
        # 1. Panel de formulario
        self.form = ProductForm(tab, on_save=self.handle_save)
        self.form.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        # 2. Panel de listado
        self.product_list = self._list_panel(tab, "Catálogo de Productos")

    def _build_methods_tab(self, tab):
        self._two_columns(tab)
        self.method_form = PaymentMethodForm(tab, on_save=self.handle_save_method)
        self.method_form.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.method_list = self._list_panel(tab, "Métodos de Pago")

    def _build_prices_tab(self, tab):
        self._two_columns(tab)
        self.price_form = PriceForm(tab, on_save=self.handle_save_price,
                                    on_product_change=self.show_price_list)
        self.price_form.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.price_list = self._list_panel(tab, "Precio final por método de pago")

    # ------------------------------------------------------------------ carga
    def refresh(self):
        """Se llama cada vez que la vista se muestra: recarga las tres tablas juntas."""
        data, err = ProductService.load_catalog()
        if err:
            for f in (self.form, self.method_form, self.price_form):
                f.set_status(err, is_error=True)
            return
        self.catalog = data
        self._render_products()
        self._render_methods()
        self.price_form.set_options(data["products"], data["methods"])

    def _clear(self, container):
        for widget in container.winfo_children():
            widget.destroy()

    def _render_products(self):
        self._clear(self.product_list)
        products = self.catalog["products"]
        if not products:
            ctk.CTkLabel(self.product_list, text="No hay productos registrados.",
                         text_color=COLORS["muted_text"]).pack(pady=20)
            return
        for prod in products:
            card = ProductCard(self.product_list, product=prod,
                               on_edit=self.form.populate,
                               on_delete=self.handle_delete,
                               on_restock=self.handle_restock)
            card.pack(fill="x", padx=5, pady=5)

    def _render_methods(self):
        self._clear(self.method_list)
        methods = self.catalog["methods"]
        if not methods:
            ctk.CTkLabel(self.method_list, text="No hay métodos de pago registrados.",
                         text_color=COLORS["muted_text"]).pack(pady=20)
            return
        for method in methods:
            card = PaymentMethodCard(self.method_list, method=method,
                                     on_edit=self.method_form.populate,
                                     on_delete=self.handle_delete_method)
            card.pack(fill="x", padx=5, pady=5)

    # ------------------------------------------------------------------ catálogo
    def handle_save(self, prod_id: Optional[int], data: Dict, stock: int):
        if prod_id is None:
            _, err = ProductService.create_product(data, stock)
            success_msg = "Producto agregado correctamente."
        else:
            _, err = ProductService.update_product(prod_id, data)
            success_msg = "Producto actualizado correctamente."

        if err:
            self.form.set_status(err, is_error=True)
            return

        self.form.clear()
        self.form.set_status(success_msg)
        self.refresh()

    def handle_delete(self, product_id: int):
        name = next((p["name"] for p in self.catalog["products"] if p["product_id"] == product_id),
                    f"#{product_id}")
        if not messagebox.askyesno("Confirmar", f"¿Estás seguro de eliminar '{name}'?", parent=self):
            return

        ok, err = ProductService.delete_product(product_id)
        if not ok:
            self.form.set_status(err or "Error al eliminar.", is_error=True)
            return

        self.form.clear()  # evita que quede cargado un producto que ya no existe
        self.form.set_status("Producto eliminado.")
        self.refresh()

    def handle_restock(self, product_id: int, quantity: int):
        _, err = ProductService.add_stock(product_id, quantity)
        if err:
            self.form.set_status(err, is_error=True)
            return
        self.form.set_status(f"Stock repuesto: +{quantity}.")
        self.refresh()

    # ------------------------------------------------------------------ métodos de pago
    def handle_save_method(self, method_id: Optional[int], data: Dict):
        if method_id is None:
            _, err = ProductService.create_method(data)
            success_msg = "Método de pago agregado."
        else:
            _, err = ProductService.update_method(method_id, data)
            success_msg = "Método de pago actualizado."

        if err:
            self.method_form.set_status(err, is_error=True)
            return

        self.method_form.clear()
        self.method_form.set_status(success_msg)
        self.refresh()

    def handle_delete_method(self, method_id: int):
        if not messagebox.askyesno("Confirmar", f"¿Eliminar el método de pago #{method_id}?", parent=self):
            return
        ok, err = ProductService.delete_method(method_id)
        if not ok:
            self.method_form.set_status(err or "Error al eliminar.", is_error=True)
            return
        self.method_form.clear()
        self.method_form.set_status("Método de pago eliminado.")
        self.refresh()

    # ------------------------------------------------------------------ precios
    def handle_save_price(self, product_id: int, method_id: int, price: float):
        _, err = ProductService.save_base_price(product_id, method_id, price)
        if err:
            self.price_form.set_status(err, is_error=True)
            return

        selected = self.price_form.menu_product.get()   # para no perder el producto elegido
        self.refresh()
        if selected in self.price_form._products:
            self.price_form.menu_product.set(selected)
            self.price_form._product_changed(selected)
        self.price_form.set_status("Precio base guardado.")

    def show_price_list(self, product_id: int):
        """Tabla de solo lectura: precio final = base x (1 + recargo)."""
        self._clear(self.price_list)
        data, err = ProductService.price_list(product_id)
        if err:   # por ejemplo, el producto todavía no tiene precio base
            ctk.CTkLabel(self.price_list, text=err, text_color=COLORS["status_err"],
                         wraplength=380, justify="left").pack(pady=20, padx=10)
            return

        ctk.CTkLabel(self.price_list,
                     text=f"{data['name']}  |  Base: ${data['base_price']:,.2f} {data['currency']}",
                     font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="w", padx=5, pady=(0, 10))
        for p in data["prices"]:
            row = ctk.CTkFrame(self.price_list, corner_radius=8, fg_color=COLORS["bg_card"])
            row.pack(fill="x", padx=5, pady=3)
            ctk.CTkLabel(row, text=f"{p['method_name']}   (recargo {p['overload'] * 100:g}%)",
                         anchor="w").pack(side="left", padx=15, pady=8)
            ctk.CTkLabel(row, text=f"${p['final_price']:,.2f}",
                         font=ctk.CTkFont(size=14, weight="bold")).pack(side="right", padx=15, pady=8)