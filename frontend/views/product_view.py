"""
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
Vista principal del catálogo de productos. 
Integra el formulario de creación/edición con una lista deslizable de tarjetas de productos, 
sincronizando los cambios con la capa de servicio.
"""

import customtkinter as ctk
from tkinter import messagebox

from typing import Optional, Dict

from frontend.services.product_service import ProductService
from frontend.components.forms import ProductForm
from frontend.components.cards import ProductCard
from frontend.config import COLORS

class ProductView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # 1. Panel de Formulario
        self.form = ProductForm(self, on_save=self.handle_save)
        self.form.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")

        # 2. Panel de Listado
        self.list_container = ctk.CTkFrame(self, corner_radius=10)
        self.list_container.grid(row=0, column=1, padx=(0, 15), pady=15, sticky="nsew")

        header_frame = ctk.CTkFrame(self.list_container, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=15)

        title = ctk.CTkLabel(header_frame, text="Catálogo de Productos", font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(side="left")

        btn_refresh = ctk.CTkButton(header_frame, text="Actualizar", width=90, command=self.load_data)
        btn_refresh.pack(side="right")

        self.scroll_area = ctk.CTkScrollableFrame(self.list_container)
        self.scroll_area.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        self.load_data()

    def load_data(self):
        for widget in self.scroll_area.winfo_children():
            widget.destroy()

        products, err = ProductService.get_all()
        if err:
            self.form.set_status(err, is_error=True)
            return

        if not products:
            empty_lbl = ctk.CTkLabel(self.scroll_area, text="No hay productos registrados.", text_color=COLORS["muted_text"])
            empty_lbl.pack(pady=20)
            return

        for prod in products:
            card = ProductCard(
                self.scroll_area,
                product=prod,
                on_edit=self.form.populate,
                on_delete=self.handle_delete
            )
            card.pack(fill="x", padx=5, pady=5)

    def handle_save(self, prod_id: Optional[int], name: str, price: float, stock: int):
        if prod_id is None:
            _, err = ProductService.create(name, price, stock)
            success_msg = "Producto agregado correctamente."
        else:
            _, err = ProductService.update(prod_id, name, price, stock)
            success_msg = "Producto actualizado correctamente."

        if err:
            self.form.set_status(err, is_error=True)
            return

        self.form.set_status(success_msg)
        self.form.clear()
        self.load_data()

    def handle_delete(self, product_id: int):
        confirm = messagebox.askyesno("Confirmar", f"¿Estás seguro de eliminar el producto #{product_id}?")
        if not confirm:
            return

        ok, err = ProductService.delete(product_id)
        if not ok:
            self.form.set_status(err or "Error al eliminar.", is_error=True)
            return

        self.form.set_status("Producto eliminado.")
        self.load_data()

    def refresh(self):
        self.load_data()