"""
/app/controllers/product_controller.py
Reglas: datos limpios, sin duplicados (nombre + tamaño), el stock solo cambia por
reposición o por pedidos, y no se borra un producto con reservas o pedidos.
"""
import sqlite3

from app.controllers.common_controller import (conflict, not_found, non_negative_int, optional_text, positive_int, required_text, transaction)
from app.models.product_model import ProductModel
from app.models.product_payment_model import ProductPaymentModel
from app.models.order_detail_model import OrderDetailModel


class ProductController:
    OPTIONAL = ("ingredients", "taste", "texture",
                "product_subcategory", "product_group", "product_subgroup")

    @staticmethod
    def _present(row: sqlite3.Row) -> dict:
        data = dict(row)
        data["available"] = data["stock"] - data["reserved_stock"]  # lo que realmente se puede vender
        return data

    @staticmethod
    def _row(db: sqlite3.Connection, product_id: int) -> sqlite3.Row:
        row = ProductModel.get_by_id(db, product_id)
        if row is None:
            raise not_found("Producto", product_id)
        return row

    @staticmethod
    def _clean(db: sqlite3.Connection, data: dict, exclude_id: int | None = None) -> dict:
        clean = {
            "name": required_text(data.get("name"), "name"),
            "description": required_text(data.get("description"), "description"),
            "size": required_text(data.get("size"), "size"),
            "product_category": required_text(data.get("product_category"), "product_category"),
        }
        for field in ProductController.OPTIONAL:
            clean[field] = optional_text(data.get(field), field)
        if ProductModel.exists_name_size(db, clean["name"], clean["size"], exclude_id):
            raise conflict(f"Ya existe '{clean['name']}' en tamaño '{clean['size']}'")
        return clean

    @staticmethod
    def get_all(db: sqlite3.Connection) -> list[dict]:
        return [ProductController._present(r) for r in ProductModel.get_all(db)]

    @staticmethod
    def get(db: sqlite3.Connection, product_id: int) -> dict:
        return ProductController._present(ProductController._row(db, product_id))

    @staticmethod
    def create(db: sqlite3.Connection, data: dict) -> dict:
        clean = ProductController._clean(db, data)
        clean["stock"] = non_negative_int(data.get("stock") or 0, "stock")
        # reserved_stock nunca lo define el cliente: el modelo siempre inserta 0
        with transaction(db):
            new_id = ProductModel.create(db, clean)
        return ProductController.get(db, new_id)

    @staticmethod
    def update(db: sqlite3.Connection, product_id: int, data: dict) -> dict:
        ProductController._row(db, product_id)
        clean = ProductController._clean(db, data, exclude_id=product_id)
        with transaction(db):   # el modelo no toca stock ni reserved_stock
            ProductModel.update(db, product_id, clean)
        return ProductController.get(db, product_id)

    @staticmethod
    def add_stock(db: sqlite3.Connection, product_id: int, quantity: int) -> dict:
        ProductController._row(db, product_id)
        qty = positive_int(quantity, "quantity")
        with transaction(db):
            ProductModel.increase_stock(db, product_id, qty)
        return ProductController.get(db, product_id)

    @staticmethod
    def delete(db: sqlite3.Connection, product_id: int) -> dict:
        product = ProductController._row(db, product_id)
        if product["reserved_stock"] > 0:
            raise conflict("El producto tiene unidades reservadas en pedidos pendientes")
        if OrderDetailModel.count_by_product(db, product_id) > 0:
            raise conflict("El producto tiene pedidos asociados: no se puede eliminar")
        deleted = ProductController._present(product)
        with transaction(db):
            ProductPaymentModel.delete_by_product(db, product_id)  # su precio base no bloquea el borrado
            ProductModel.delete(db, product_id)
        return deleted