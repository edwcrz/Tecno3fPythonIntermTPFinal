"""
/app/controllers/search_controller.py
Buscadores:
- Cliente por email: búsqueda EXACTA, resultado único.
- Producto e ingrediente: búsqueda ENMASCARADA (%texto%) resuelta en SQL con LIKE.
Si hay varias palabras, deben estar todas.
"""
import sqlite3

from fastapi import HTTPException, status

from app.controllers.common_controller import EMAIL_RE, invalid, required_text
from app.controllers.customer_controller import CustomerController
from app.controllers.product_controller import ProductController
from app.models.customer_model import CustomerModel
from app.models.product_model import ProductModel
from app.models.product_payment_model import ProductPaymentModel

NAME_FIELDS = ("name", "product_category", "product_subcategory", "product_group", "product_subgroup")
INGREDIENT_FIELDS = ("ingredients",)


class SearchController:

    # ---------- búsqueda exacta ----------
    @staticmethod
    def customer_by_email(db: sqlite3.Connection, email: str) -> dict:
        email = required_text(email, "email", 120).lower()
        if not EMAIL_RE.match(email):
            raise invalid("El email no tiene un formato válido")
        row = CustomerModel.get_by_email(db, email)
        if row is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "No hay ningún cliente con ese email")

        customer = CustomerController.get(db, row["customer_id"])
        try:
            CustomerController.validate_can_buy(db, row["customer_id"])
            customer["can_buy"], customer["reason"] = True, "Puede comprar"
        except HTTPException as e:   # misma regla que el pedido: falta email o dirección
            customer["can_buy"], customer["reason"] = False, str(e.detail)
        return customer

    # ---------- búsqueda enmascarada ----------
    @staticmethod
    def _search_products(db: sqlite3.Connection, query: str, fields: tuple) -> dict:
        text = required_text(query, "búsqueda", 100)
        if len(text.replace(" ", "")) < 2:
            raise invalid("Escribí al menos 2 letras")

        results = []
        for row in ProductModel.search_like(db, text, fields):
            item = ProductController._present(row)          # trae 'available'
            base = ProductPaymentModel.get_by_product(db, row["product_id"])
            item["base_price"] = base["price"] if base else None
            item["sellable"] = base is not None and item["available"] > 0
            results.append(item)

        results.sort(key=lambda p: (not p["sellable"], p["name"].lower(), p["size"].lower()))
        return {"query": text, "total": len(results), "results": results}

    @staticmethod
    def products(db: sqlite3.Connection, query: str) -> dict:
        return SearchController._search_products(db, query, NAME_FIELDS)

    @staticmethod
    def ingredient(db: sqlite3.Connection, query: str) -> dict:
        return SearchController._search_products(db, query, INGREDIENT_FIELDS)