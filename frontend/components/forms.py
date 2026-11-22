"""
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
from typing import Callable, Optional, Dict, List
from frontend.config import COLORS

# (clave del backend, texto del placeholder)
REQUIRED_FIELDS = [
    ("name", "Nombre del producto"),
    ("description", "Descripción"),
    ("size", "Tamaño (ej: Individual, Grande)"),
    ("product_category", "Categoría (ej: Tortas, Cookies)"),
]
OPTIONAL_FIELDS = [
    ("ingredients", "Ingredientes (opcional)"),
    ("taste", "Sabor (opcional)"),
    ("texture", "Textura (opcional)"),
    ("product_subcategory", "Subcategoría (opcional)"),
    ("product_group", "Grupo (opcional)"),
    ("product_subgroup", "Subgrupo (opcional)"),
]


class ProductForm(ctk.CTkScrollableFrame):
    # on_save recibe: id (None si es alta), datos del producto, stock inicial (solo al crear)
    def __init__(self, master, on_save: Callable[[Optional[int], Dict, int], None]):
        super().__init__(master, corner_radius=10)
        self.on_save = on_save
        self.current_editing_id: Optional[int] = None
        self.entries: Dict[str, ctk.CTkEntry] = {}

        self.title_lbl = ctk.CTkLabel(self, text="Datos del Producto", font=ctk.CTkFont(size=18, weight="bold"))
        self.title_lbl.pack(padx=20, pady=(20, 15))

        for key, placeholder in REQUIRED_FIELDS + OPTIONAL_FIELDS:
            entry = ctk.CTkEntry(self, placeholder_text=placeholder)
            entry.pack(padx=20, pady=6, fill="x")
            self.entries[key] = entry

        # El stock solo se carga al crear; después se repone desde la tarjeta
        self.txt_stock = ctk.CTkEntry(self, placeholder_text="Stock inicial (ej: 10)")
        self.txt_stock.pack(padx=20, pady=6, fill="x")

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

        self.status_lbl = ctk.CTkLabel(self, text="", text_color=COLORS["status_ok"], wraplength=240)
        self.status_lbl.pack(padx=20, pady=12)

    def _handle_save(self):
        data = {key: entry.get().strip() for key, entry in self.entries.items()}

        for key, _ in REQUIRED_FIELDS:
            if not data[key]:
                self.set_status("Nombre, descripción, tamaño y categoría son obligatorios.", is_error=True)
                return

        stock = 0
        if self.current_editing_id is None:   # en edición el stock no se envía
            stock_raw = self.txt_stock.get().strip() or "0"
            try:
                stock = int(stock_raw)
            except ValueError:
                self.set_status("El stock debe ser un número entero.", is_error=True)
                return
            if stock < 0:
                self.set_status("El stock no puede ser negativo.", is_error=True)
                return

        self.on_save(self.current_editing_id, data, stock)

    def populate(self, product: Dict):
        self.current_editing_id = product["product_id"]
        for key, entry in self.entries.items():
            entry.delete(0, "end")
            entry.insert(0, product.get(key) or "")

        # Se muestra el stock actual pero bloqueado: se repone desde la tarjeta
        self.txt_stock.configure(state="normal")
        self.txt_stock.delete(0, "end")
        self.txt_stock.insert(0, str(product["stock"]))
        self.txt_stock.configure(state="disabled")

        self.btn_save.configure(text="Guardar Cambios", fg_color=COLORS["success"])
        self.btn_cancel.pack(padx=20, pady=(5, 0), fill="x", after=self.btn_save)
        self.set_status(f"Modificando producto #{product['product_id']}")

    def clear(self):
        self.current_editing_id = None
        for entry in self.entries.values():
            entry.delete(0, "end")
        self.txt_stock.configure(state="normal")
        self.txt_stock.delete(0, "end")
        self.btn_save.configure(text="Agregar Producto", fg_color=COLORS["primary"])
        self.btn_cancel.pack_forget()

    def set_status(self, text: str, is_error: bool = False):
        self.status_lbl.configure(
            text=text,
            text_color=COLORS["status_err"] if is_error else COLORS["status_ok"]
        )


class PaymentMethodForm(ctk.CTkFrame):
    """Método de pago. El recargo se escribe en % (10) y se envía como fracción (0.10)."""
    def __init__(self, master, on_save: Callable[[Optional[int], Dict], None]):
        super().__init__(master, corner_radius=10)
        self.on_save = on_save
        self.current_editing_id: Optional[int] = None

        ctk.CTkLabel(self, text="Método de Pago", font=ctk.CTkFont(size=18, weight="bold")).pack(padx=20, pady=(20, 15))

        self.txt_name = ctk.CTkEntry(self, placeholder_text="Nombre (ej: Tarjeta de crédito)")
        self.txt_name.pack(padx=20, pady=6, fill="x")
        self.txt_overload = ctk.CTkEntry(self, placeholder_text="Recargo en % (ej: 10)")
        self.txt_overload.pack(padx=20, pady=6, fill="x")
        self.txt_term = ctk.CTkEntry(self, placeholder_text="Plazo en días (opcional, 0 por defecto)")
        self.txt_term.pack(padx=20, pady=6, fill="x")
        self.txt_category = ctk.CTkEntry(self, placeholder_text="Categoría (opcional)")
        self.txt_category.pack(padx=20, pady=6, fill="x")
        self.txt_subcategory = ctk.CTkEntry(self, placeholder_text="Subcategoría (opcional)")
        self.txt_subcategory.pack(padx=20, pady=6, fill="x")

        self.btn_save = ctk.CTkButton(self, text="Agregar Método", command=self._handle_save,
                                      fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"])
        self.btn_save.pack(padx=20, pady=(15, 5), fill="x")
        self.btn_cancel = ctk.CTkButton(self, text="Cancelar Edición", command=self.clear,
                                        fg_color=COLORS["cancel"], hover_color=COLORS["cancel_hover"])
        self.status_lbl = ctk.CTkLabel(self, text="", text_color=COLORS["status_ok"], wraplength=240)
        self.status_lbl.pack(padx=20, pady=12)

    def _handle_save(self):
        name = self.txt_name.get().strip()
        if not name:
            self.set_status("El nombre es obligatorio.", is_error=True)
            return
        try:
            percent = float((self.txt_overload.get().strip() or "0").replace(",", "."))
            term = int(self.txt_term.get().strip() or "0")
        except ValueError:
            self.set_status("Recargo o plazo con formato inválido.", is_error=True)
            return
        if not 0 <= percent <= 100 or term < 0:
            self.set_status("El recargo va de 0 a 100 y el plazo no puede ser negativo.", is_error=True)
            return

        data = {
            "method_name": name,
            "overload": round(percent / 100, 4),   # 10 (%) -> 0.10
            "payment_term": term,
            "payment_category": self.txt_category.get().strip(),
            "payment_subcategory": self.txt_subcategory.get().strip(),
        }
        self.on_save(self.current_editing_id, data)

    def populate(self, method: Dict):
        self.current_editing_id = method["payment_method_id"]
        values = [
            (self.txt_name, method["method_name"]),
            (self.txt_overload, f"{method['overload'] * 100:g}"),   # 0.10 -> 10
            (self.txt_term, str(method["payment_term"])),
            (self.txt_category, method.get("payment_category") or ""),
            (self.txt_subcategory, method.get("payment_subcategory") or ""),
        ]
        for entry, value in values:
            entry.delete(0, "end")
            entry.insert(0, value)
        self.btn_save.configure(text="Guardar Cambios", fg_color=COLORS["success"])
        self.btn_cancel.pack(padx=20, pady=(5, 0), fill="x", after=self.btn_save)
        self.set_status(f"Modificando método #{method['payment_method_id']}")

    def clear(self):
        self.current_editing_id = None
        for entry in (self.txt_name, self.txt_overload, self.txt_term, self.txt_category, self.txt_subcategory):
            entry.delete(0, "end")
        self.btn_save.configure(text="Agregar Método", fg_color=COLORS["primary"])
        self.btn_cancel.pack_forget()

    def set_status(self, text: str, is_error: bool = False):
        self.status_lbl.configure(text=text,
                                  text_color=COLORS["status_err"] if is_error else COLORS["status_ok"])


class PriceForm(ctk.CTkFrame):
    """
    Precio base de un producto. Se carga con un método SIN recargo (Efectivo, Transferencia, QR).
    El precio final de los demás métodos se calcula: base x (1 + recargo).
    """
    NO_DATA = "(sin datos)"

    def __init__(self, master, on_save: Callable[[int, int, float], None],
                 on_product_change: Optional[Callable[[int], None]] = None):
        super().__init__(master, corner_radius=10)
        self.on_save = on_save
        self.on_product_change = on_product_change
        self._products: Dict[str, Dict] = {}
        self._methods: Dict[str, Dict] = {}

        ctk.CTkLabel(self, text="Precio Base", font=ctk.CTkFont(size=18, weight="bold")).pack(padx=20, pady=(20, 15))

        self.menu_product = ctk.CTkOptionMenu(self, values=[self.NO_DATA], command=self._product_changed)
        self.menu_product.pack(padx=20, pady=6, fill="x")
        self.menu_method = ctk.CTkOptionMenu(self, values=[self.NO_DATA])
        self.menu_method.pack(padx=20, pady=6, fill="x")
        self.txt_price = ctk.CTkEntry(self, placeholder_text="Precio base (ej: 2500)")
        self.txt_price.pack(padx=20, pady=6, fill="x")

        self.btn_save = ctk.CTkButton(self, text="Guardar Precio", command=self._handle_save,
                                      fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"])
        self.btn_save.pack(padx=20, pady=(15, 5), fill="x")
        self.status_lbl = ctk.CTkLabel(self, text="", text_color=COLORS["status_ok"], wraplength=240)
        self.status_lbl.pack(padx=20, pady=12)

    def set_options(self, products: List[Dict], methods: List[Dict]):
        """Se llama en cada refresh. Solo ofrece métodos sin recargo."""
        self._products = {f"#{p['product_id']} {p['name']} ({p['size']})": p for p in products}
        self._methods = {m["method_name"]: m for m in methods if m["overload"] == 0}
        product_labels = list(self._products) or [self.NO_DATA]
        method_labels = list(self._methods) or [self.NO_DATA]
        self.menu_product.configure(values=product_labels)
        self.menu_method.configure(values=method_labels)
        self.menu_product.set(product_labels[0])
        self.menu_method.set(method_labels[0])
        self._product_changed(product_labels[0])

    def _product_changed(self, label: str):
        product = self._products.get(label)
        self.txt_price.delete(0, "end")
        if product and product.get("base_price") is not None:
            self.txt_price.insert(0, str(product["base_price"]))
        if product and self.on_product_change:
            self.on_product_change(product["product_id"])

    def _handle_save(self):
        product = self._products.get(self.menu_product.get())
        method = self._methods.get(self.menu_method.get())
        if not product or not method:
            self.set_status("Elegí un producto y un método sin recargo.", is_error=True)
            return
        try:
            price = float(self.txt_price.get().strip().replace(",", "."))
        except ValueError:
            self.set_status("El precio debe ser un número.", is_error=True)
            return
        if price < 0.01:
            self.set_status("El precio debe ser al menos 0.01.", is_error=True)
            return
        self.on_save(product["product_id"], method["payment_method_id"], price)

    def set_status(self, text: str, is_error: bool = False):
        self.status_lbl.configure(text=text, text_color=COLORS["status_err"] if is_error else COLORS["status_ok"])

class CustomerForm(ctk.CTkScrollableFrame):
    """Datos del cliente. Para vender hace falta email y al menos una dirección."""
    FIELDS = [
        ("name", "Nombre (obligatorio)"),
        ("surname", "Apellido"),
        ("nickname", "Apodo"),
        ("email", "Email (necesario para vender)"),
        ("instagram", "Instagram (ej: @ana.dulces)"),
        ("phone", "Teléfono (ej: +54 11 1234-5678)"),
        ("age", "Edad (0 a 120)"),
        ("gender", "Género"),
        ("likes", "Likes (número, opcional)"),
        ("notes", "Notas"),
    ]

    # on_save recibe: id (None si es alta) y los datos del cliente
    def __init__(self, master, on_save: Callable[[Optional[int], Dict], None]):
        super().__init__(master, corner_radius=10)
        self.on_save = on_save
        self.current_editing_id: Optional[int] = None
        self.entries: Dict[str, ctk.CTkEntry] = {}

        ctk.CTkLabel(self, text="Datos del Cliente", font=ctk.CTkFont(size=18, weight="bold")).pack(
            padx=20, pady=(20, 15))
        for key, placeholder in self.FIELDS:
            entry = ctk.CTkEntry(self, placeholder_text=placeholder)
            entry.pack(padx=20, pady=6, fill="x")
            self.entries[key] = entry

        self.btn_save = ctk.CTkButton(self, text="Agregar Cliente", command=self._handle_save,
                                      fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"])
        self.btn_save.pack(padx=20, pady=(15, 5), fill="x")
        self.btn_cancel = ctk.CTkButton(self, text="Cancelar Edición", command=self.clear,
                                        fg_color=COLORS["cancel"], hover_color=COLORS["cancel_hover"])
        self.status_lbl = ctk.CTkLabel(self, text="", text_color=COLORS["status_ok"], wraplength=240)
        self.status_lbl.pack(padx=20, pady=12)

    def _handle_save(self):
        data = {key: entry.get().strip() for key, entry in self.entries.items()}
        if not data["name"]:
            self.set_status("El nombre es obligatorio.", is_error=True)
            return
        if data["email"] and ("@" not in data["email"] or "." not in data["email"].split("@")[-1]):
            self.set_status("El email no tiene un formato válido.", is_error=True)
            return
        if data["age"] and (not data["age"].isdigit() or int(data["age"]) > 120):
            self.set_status("La edad debe ser un número entre 0 y 120.", is_error=True)
            return
        if data["likes"] and not data["likes"].isdigit():
            self.set_status("Los likes deben ser un número entero.", is_error=True)
            return
        self.on_save(self.current_editing_id, data)

    def populate(self, customer: Dict):
        self.current_editing_id = customer["customer_id"]
        for key, entry in self.entries.items():
            entry.delete(0, "end")
            value = customer.get(key)
            entry.insert(0, "" if value is None else str(value))
        self.btn_save.configure(text="Guardar Cambios", fg_color=COLORS["success"])
        self.btn_cancel.pack(padx=20, pady=(5, 0), fill="x", after=self.btn_save)
        self.set_status(f"Modificando cliente #{customer['customer_id']}")

    def clear(self):
        self.current_editing_id = None
        for entry in self.entries.values():
            entry.delete(0, "end")
        self.btn_save.configure(text="Agregar Cliente", fg_color=COLORS["primary"])
        self.btn_cancel.pack_forget()

    def set_status(self, text: str, is_error: bool = False):
        self.status_lbl.configure(text=text,
                                  text_color=COLORS["status_err"] if is_error else COLORS["status_ok"])


class AddressForm(ctk.CTkScrollableFrame):
    """Dirección de delivery. Primero se elige el cliente; la dirección no cambia de cliente."""
    NO_DATA = "(sin clientes)"
    FIELDS = [
        ("address", "Dirección (obligatorio)"),
        ("locality", "Localidad"),
        ("province", "Provincia"),
        ("country", "País"),
        ("postal_code", "Código postal"),
        ("notes", "Notas (ej: tocar timbre 3B)"),
    ]

    # on_save recibe: id del cliente, id de la dirección (None si es alta), datos
    def __init__(self, master, on_save: Callable[[int, Optional[int], Dict], None],
                 on_customer_change: Optional[Callable[[int], None]] = None):
        super().__init__(master, corner_radius=10)
        self.on_save = on_save
        self.on_customer_change = on_customer_change
        self.current_editing_id: Optional[int] = None
        self._customers: Dict[str, Dict] = {}
        self.entries: Dict[str, ctk.CTkEntry] = {}

        ctk.CTkLabel(self, text="Dirección de Entrega", font=ctk.CTkFont(size=18, weight="bold")).pack(
            padx=20, pady=(20, 15))
        self.menu_customer = ctk.CTkOptionMenu(self, values=[self.NO_DATA], command=self._customer_changed)
        self.menu_customer.pack(padx=20, pady=6, fill="x")
        for key, placeholder in self.FIELDS:
            entry = ctk.CTkEntry(self, placeholder_text=placeholder)
            entry.pack(padx=20, pady=6, fill="x")
            self.entries[key] = entry

        self.btn_save = ctk.CTkButton(self, text="Agregar Dirección", command=self._handle_save,
                                      fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"])
        self.btn_save.pack(padx=20, pady=(15, 5), fill="x")
        self.btn_cancel = ctk.CTkButton(self, text="Cancelar Edición", command=self.clear,
                                        fg_color=COLORS["cancel"], hover_color=COLORS["cancel_hover"])
        self.status_lbl = ctk.CTkLabel(self, text="", text_color=COLORS["status_ok"], wraplength=240)
        self.status_lbl.pack(padx=20, pady=12)

    @staticmethod
    def _label(c: Dict) -> str:
        return f"#{c['customer_id']} {c['name']} {c.get('surname') or ''}".strip()

    def set_customers(self, customers: List[Dict], selected_id: Optional[int] = None):
        """Se llama en cada refresh; conserva el cliente elegido."""
        self._customers = {self._label(c): c for c in customers}
        labels = list(self._customers) or [self.NO_DATA]
        self.menu_customer.configure(values=labels)
        chosen = next((l for l, c in self._customers.items() if c["customer_id"] == selected_id), labels[0])
        self.menu_customer.set(chosen)
        self._customer_changed(chosen)

    def select_customer(self, customer_id: int):
        label = next((l for l, c in self._customers.items() if c["customer_id"] == customer_id), None)
        if label:
            self.menu_customer.set(label)
            self._customer_changed(label)

    def _customer_changed(self, label: str):
        customer = self._customers.get(label)
        if customer and self.on_customer_change:
            self.on_customer_change(customer["customer_id"])

    def _handle_save(self):
        customer = self._customers.get(self.menu_customer.get())
        if not customer:
            self.set_status("Elegí un cliente.", is_error=True)
            return
        data = {key: entry.get().strip() for key, entry in self.entries.items()}
        if not data["address"]:
            self.set_status("La dirección es obligatoria.", is_error=True)
            return
        self.on_save(customer["customer_id"], self.current_editing_id, data)

    def populate(self, address: Dict):
        self.current_editing_id = address["address_id"]
        for key, entry in self.entries.items():
            entry.delete(0, "end")
            entry.insert(0, address.get(key) or "")
        self.menu_customer.configure(state="disabled")   # la dirección no cambia de cliente
        self.btn_save.configure(text="Guardar Cambios", fg_color=COLORS["success"])
        self.btn_cancel.pack(padx=20, pady=(5, 0), fill="x", after=self.btn_save)
        self.set_status(f"Modificando dirección #{address['address_id']}")

    def clear(self):
        self.current_editing_id = None
        for entry in self.entries.values():
            entry.delete(0, "end")
        self.menu_customer.configure(state="normal")
        self.btn_save.configure(text="Agregar Dirección", fg_color=COLORS["primary"])
        self.btn_cancel.pack_forget()

    def set_status(self, text: str, is_error: bool = False):
        self.status_lbl.configure(text=text, text_color=COLORS["status_err"] if is_error else COLORS["status_ok"])