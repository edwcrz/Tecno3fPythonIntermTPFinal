"""
Vista especializada en el registro y listado de Clientes. 
Gestiona la entrada de datos (nombre, email, teléfono) y 
captura posibles errores de integridad relacional al intentar eliminar clientes activos.
"""

"""
/frontend/views/customer_view.py
Pantalla CLIENTES. Agrupa dos tablas del backend en dos pestañas:
- Clientes: customer (formulario + tarjetas con la marca "Puede comprar / Falta email / Falta dirección")
- Direcciones: customer_address (direcciones de delivery del cliente elegido)
La dirección se lee del cliente: no se copia a los pedidos.
"""

from typing import Dict, List, Optional
from tkinter import messagebox

import customtkinter as ctk

from frontend.services.customer_service import CustomerService
from frontend.components.forms import CustomerForm, AddressForm
from frontend.components.cards import CustomerCard, AddressCard
from frontend.views.base_view import BaseView
from frontend.config import COLORS


class CustomerView(BaseView):
    def __init__(self, master):
        super().__init__(master)
        self.customers: List[Dict] = []
        self.selected_customer_id: Optional[int] = None

        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=10, pady=(10, 0))
        ctk.CTkLabel(top, text="Clientes", font=ctk.CTkFont(size=20, weight="bold")).pack(side="left")
        ctk.CTkButton(top, text="Actualizar", width=90, command=self.refresh).pack(side="right")

        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(fill="both", expand=True, padx=5, pady=5)
        self._build_customer_tab(self.tabs.add("Clientes"))
        self._build_address_tab(self.tabs.add("Direcciones"))
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

    def _build_customer_tab(self, tab):
        self._two_columns(tab)
        self.form = CustomerForm(tab, on_save=self.handle_save)
        self.form.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.customer_list = self._list_panel(tab, "Lista de Clientes")

    def _build_address_tab(self, tab):
        self._two_columns(tab)
        self.address_form = AddressForm(tab, on_save=self.handle_save_address,
                                        on_customer_change=self.show_addresses)
        self.address_form.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.address_list = self._list_panel(tab, "Direcciones del cliente")

    # ------------------------------------------------------------------ carga
    def refresh(self):
        """Se llama cada vez que la vista se muestra: recarga clientes (ya traen sus direcciones)."""
        customers, err = CustomerService.list_customers()
        if err:
            self.form.set_status(err, is_error=True)
            self.address_form.set_status(err, is_error=True)
            return
        self.customers = customers
        self._render_customers()
        self.address_form.set_customers(customers, self.selected_customer_id)

    def _clear(self, container):
        for widget in container.winfo_children():
            widget.destroy()

    def _render_customers(self):
        self._clear(self.customer_list)
        if not self.customers:
            ctk.CTkLabel(self.customer_list, text="No hay clientes registrados.",
                         text_color=COLORS["muted_text"]).pack(pady=20)
            return
        for customer in self.customers:
            can_buy, reason = CustomerService.sale_status(customer)
            card = CustomerCard(self.customer_list, customer=customer, can_buy=can_buy, reason=reason,
                                on_edit=self.form.populate,
                                on_delete=self.handle_delete,
                                on_addresses=self.go_to_addresses)
            card.pack(fill="x", padx=5, pady=5)

    # ------------------------------------------------------------------ clientes
    def handle_save(self, customer_id: Optional[int], data: Dict):
        if customer_id is None:
            _, err = CustomerService.create_customer(data)
            success_msg = "Cliente agregado correctamente."
        else:
            _, err = CustomerService.update_customer(customer_id, data)
            success_msg = "Cliente actualizado correctamente."

        if err:
            self.form.set_status(err, is_error=True)
            return

        self.form.clear()
        self.form.set_status(success_msg)
        self.refresh()

    def handle_delete(self, customer_id: int):
        customer = next((c for c in self.customers if c["customer_id"] == customer_id), None)
        name = customer["name"] if customer else f"#{customer_id}"
        if not messagebox.askyesno("Confirmar", f"¿Eliminar al cliente '{name}' y sus direcciones?", parent=self):
            return

        ok, err = CustomerService.delete_customer(customer_id)
        if not ok:   # por ejemplo: el cliente tiene pedidos (se conserva el historial)
            self.form.set_status(err or "Error al eliminar.", is_error=True)
            return

        self.form.clear()
        if self.selected_customer_id == customer_id:
            self.selected_customer_id = None
        self.form.set_status("Cliente eliminado.")
        self.refresh()

    def go_to_addresses(self, customer_id: int):
        self.tabs.set("Direcciones")
        self.address_form.select_customer(customer_id)

    # ------------------------------------------------------------------ direcciones
    def show_addresses(self, customer_id: int):
        """Lista las direcciones del cliente elegido (salen del propio cliente)."""
        self.selected_customer_id = customer_id
        self._clear(self.address_list)
        customer = next((c for c in self.customers if c["customer_id"] == customer_id), None)
        addresses = customer.get("addresses", []) if customer else []
        if not addresses:
            ctk.CTkLabel(self.address_list,
                         text="Este cliente no tiene direcciones: no se le puede vender.",
                         text_color=COLORS["status_err"], wraplength=380).pack(pady=20, padx=10)
            return
        for address in addresses:
            card = AddressCard(self.address_list, address=address,
                               on_edit=self.address_form.populate,
                               on_delete=self.handle_delete_address)
            card.pack(fill="x", padx=5, pady=5)

    def handle_save_address(self, customer_id: int, address_id: Optional[int], data: Dict):
        if address_id is None:
            _, err = CustomerService.create_address(customer_id, data)
            success_msg = "Dirección agregada correctamente."
        else:
            _, err = CustomerService.update_address(address_id, data)
            success_msg = "Dirección actualizada correctamente."

        if err:
            self.address_form.set_status(err, is_error=True)
            return

        self.address_form.clear()
        self.selected_customer_id = customer_id
        self.refresh()
        self.address_form.set_status(success_msg)

    def handle_delete_address(self, address_id: int):
        if not messagebox.askyesno("Confirmar", f"¿Eliminar la dirección #{address_id}?", parent=self):
            return
        ok, err = CustomerService.delete_address(address_id)
        if not ok:
            self.address_form.set_status(err or "Error al eliminar.", is_error=True)
            return
        self.address_form.clear()
        self.refresh()
        self.address_form.set_status("Dirección eliminada.")