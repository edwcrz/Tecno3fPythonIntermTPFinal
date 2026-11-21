"""
Vista especializada en el registro y listado de Clientes. 
Gestiona la entrada de datos (nombre, email, teléfono) y 
captura posibles errores de integridad relacional al intentar eliminar clientes activos.
"""
import customtkinter as ctk
from tkinter import messagebox
from frontend.services.customer_service import CustomerService
from frontend.config import COLORS

class CustomerView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # Formulario
        self.form_frame = ctk.CTkFrame(self, corner_radius=10)
        self.form_frame.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")

        ctk.CTkLabel(self.form_frame, text="Nuevo Cliente", font=ctk.CTkFont(size=18, weight="bold")).pack(padx=20, pady=(20, 15))
        self.txt_name = ctk.CTkEntry(self.form_frame, placeholder_text="Nombre completo")
        self.txt_name.pack(padx=20, pady=8, fill="x")

        self.txt_email = ctk.CTkEntry(self.form_frame, placeholder_text="Correo electrónico")
        self.txt_email.pack(padx=20, pady=8, fill="x")

        self.txt_phone = ctk.CTkEntry(self.form_frame, placeholder_text="Teléfono")
        self.txt_phone.pack(padx=20, pady=8, fill="x")

        btn_save = ctk.CTkButton(self.form_frame, text="Guardar Cliente", command=self.save_customer, fg_color=COLORS["primary"])
        btn_save.pack(padx=20, pady=(15, 10), fill="x")

        self.status_lbl = ctk.CTkLabel(self.form_frame, text="", text_color=COLORS["status_ok"])
        self.status_lbl.pack(padx=20, pady=10)

        # Lista
        self.list_frame = ctk.CTkFrame(self, corner_radius=10)
        self.list_frame.grid(row=0, column=1, padx=(0, 15), pady=15, sticky="nsew")

        ctk.CTkLabel(self.list_frame, text="Lista de Clientes", font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w", padx=15, pady=15)
        self.scroll = ctk.CTkScrollableFrame(self.list_frame)
        self.scroll.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        self.load_customers()

    def load_customers(self):
        for w in self.scroll.winfo_children():
            w.destroy()

        customers, err = CustomerService.get_all()
        if err:
            self.status_lbl.configure(text=err, text_color=COLORS["status_err"])
            return

        for c in customers:
            card = ctk.CTkFrame(self.scroll, corner_radius=8, fg_color=COLORS["bg_card"])
            card.pack(fill="x", padx=5, pady=5)

            ctk.CTkLabel(card, text=f"#{c['id']} {c['name']} | {c['email']} | {c['phone']}", anchor="w").pack(side="left", padx=15, pady=10, fill="x", expand=True)
            ctk.CTkButton(card, text="Eliminar", width=70, fg_color=COLORS["danger"], command=lambda cid=c["id"]: self.delete_customer(cid)).pack(side="right", padx=10, pady=8)

    def save_customer(self):
        name = self.txt_name.get().strip()
        email = self.txt_email.get().strip()
        phone = self.txt_phone.get().strip()

        if not name:
            self.status_lbl.configure(text="El nombre es obligatorio", text_color=COLORS["status_err"])
            return 
        ok, err = CustomerService.create(name, email, phone)
        if err:
            self.status_lbl.configure(text=err, text_color=COLORS["status_err"])
            return

        self.status_lbl.configure(text="Cliente creado exitosamente", text_color=COLORS["status_ok"])
        self.txt_name.delete(0, "end")
        self.txt_email.delete(0, "end")
        self.txt_phone.delete(0, "end")
        self.load_customers()

    def delete_customer(self, customer_id: int):
        if not messagebox.askyesno("Confirmar", f"¿Eliminar cliente #{customer_id}?"):
            return
        ok, err = CustomerService.delete(customer_id)
        if not ok:
            messagebox.showerror("Error", err)
            return
        self.load_customers()

    def refresh(self):
        self.load_customers()