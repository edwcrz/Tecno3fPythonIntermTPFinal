import customtkinter as ctk
from tkinter import messagebox
from frontend.services.order_service import OrderService
from frontend.services.customer_service import CustomerService
from frontend.services.product_service import ProductService
from frontend.config import COLORS

class OrderView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        self.cart_items = []
        self.customers_data = {}
        self.products_data = {}

        # Columna Izquierda: Generar Venta
        self.checkout_frame = ctk.CTkFrame(self, corner_radius=10)
        self.checkout_frame.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")

        ctk.CTkLabel(self.checkout_frame, text="Nueva Venta", font=ctk.CTkFont(size=18, weight="bold")).pack(padx=20, pady=(20, 15))

        self.cb_customers = ctk.CTkComboBox(self.checkout_frame, values=["Cargando..."])
        self.cb_customers.pack(padx=20, pady=8, fill="x")

        self.cb_products = ctk.CTkComboBox(self.checkout_frame, values=["Cargando..."])
        self.cb_products.pack(padx=20, pady=8, fill="x")

        self.txt_qty = ctk.CTkEntry(self.checkout_frame, placeholder_text="Cantidad")
        self.txt_qty.pack(padx=20, pady=8, fill="x")

        btn_add = ctk.CTkButton(self.checkout_frame, text="Agregar al Carrito", command=self.add_to_cart, fg_color=COLORS["info"])
        btn_add.pack(padx=20, pady=8, fill="x")

        self.cart_box = ctk.CTkTextbox(self.checkout_frame, height=120)
        self.cart_box.pack(padx=20, pady=8, fill="x")

        self.lbl_total = ctk.CTkLabel(self.checkout_frame, text="Total: $0.00", font=ctk.CTkFont(size=16, weight="bold"))
        self.lbl_total.pack(padx=20, pady=8)

        btn_process = ctk.CTkButton(self.checkout_frame, text="Confirmar Venta", command=self.process_sale, fg_color=COLORS["success"])
        btn_process.pack(padx=20, pady=(5, 15), fill="x")

        # Columna Derecha: Historial y Detalles
        self.history_frame = ctk.CTkFrame(self, corner_radius=10)
        self.history_frame.grid(row=0, column=1, padx=(0, 15), pady=15, sticky="nsew")

        ctk.CTkLabel(self.history_frame, text="Registro de Ventas", font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w", padx=15, pady=15)
        self.scroll = ctk.CTkScrollableFrame(self.history_frame)
        self.scroll.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        self.load_dropdowns()
        self.load_sales_history()

    def load_dropdowns(self):
        # 1. Cargar Clientes
        customers, err = CustomerService.get_all()
        if customers:
            self.customers_data = {f"#{c['id']} - {c['name']}": c["id"] for c in customers}
            self.cb_customers.configure(values=list(self.customers_data.keys()))
            self.cb_customers.set(list(self.customers_data.keys())[0])
        else:
            self.customers_data = {}
            self.cb_customers.configure(values=["Sin clientes registrados"])
            self.cb_customers.set("Sin clientes registrados")

        # 2. Cargar Productos
        prods, err = ProductService.get_all()
        if prods:
            self.products_data = {
                f"#{p['id']} {p['name']} (${p['price']})": {
                    "id": p["id"], 
                    "price": p["price"], 
                    "name": p["name"]
                } for p in prods
            }
            self.cb_products.configure(values=list(self.products_data.keys()))
            self.cb_products.set(list(self.products_data.keys())[0])
        else:
            self.products_data = {}
            self.cb_products.configure(values=["Sin stock / productos"])
            self.cb_products.set("Sin stock / productos")
            
    def add_to_cart(self):
        selected_prod = self.cb_products.get()
        qty_str = self.txt_qty.get().strip()

        if selected_prod not in self.products_data or not qty_str.isdigit():
            messagebox.showwarning("Atención", "Seleccioná un producto y una cantidad válida")
            return

        qty = int(qty_str)
        if qty <= 0:
            return

        prod_info = self.products_data[selected_prod]
        subtotal = prod_info["price"] * qty
        self.cart_items.append({"product_id": prod_info["id"], "name": prod_info["name"], "quantity": qty, "price": prod_info["price"], "subtotal": subtotal})

        self.update_cart_display()
        self.txt_qty.delete(0, "end")

    def update_cart_display(self):
        self.cart_box.delete("1.0", "end")
        total = 0.0
        for item in self.cart_items:
            self.cart_box.insert("end", f"{item['name']} x{item['quantity']} = ${item['subtotal']:.2f}\n")
            total += item["subtotal"]
        self.lbl_total.configure(text=f"Total: ${total:.2f}")

    def process_sale(self):
        selected_cust = self.cb_customers.get()
        if selected_cust not in self.customers_data or not self.cart_items:
            messagebox.showwarning("Atención", "Debe seleccionar un cliente y tener productos en el carrito")
            return

        customer_id = self.customers_data[selected_cust]
        items_payload = [{"product_id": i["product_id"], "quantity": i["quantity"]} for i in self.cart_items]

        ok, err = OrderService.create_sale(customer_id, items_payload)
        if not ok:
            messagebox.showerror("Error", err)
            return

        messagebox.showinfo("Éxito", "Venta procesada con éxito")
        self.cart_items.clear()
        self.update_cart_display()
        self.load_dropdowns()
        self.load_sales_history()

    def load_sales_history(self):
        for w in self.scroll.winfo_children():
            w.destroy()

        sales, _ = OrderService.get_all()
        if not sales:
            return

        for s in sales:
            card = ctk.CTkFrame(self.scroll, corner_radius=8, fg_color=COLORS["bg_card"])
            card.pack(fill="x", padx=5, pady=5)

            ctk.CTkLabel(card, text=f"Venta #{s['id']} | Cliente: {s['customer_name']} | Fecha: {s['date']} | Total: ${s['total']:.2f}", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=10, pady=(8, 4))

            details_text = " | ".join([f"{item['product_name']} (x{item['quantity']} a ${item['unit_price']:.2f})" for item in s["items"]])
            ctk.CTkLabel(card, text=f"Detalle: {details_text}", text_color=COLORS["muted_text"], font=ctk.CTkFont(size=12)).pack(anchor="w", padx=10, pady=(0, 8))

    def refresh(self):
        """Actualiza todos los datos de la vista al enfocarla."""
        self.load_dropdowns()
        self.load_sales_history()