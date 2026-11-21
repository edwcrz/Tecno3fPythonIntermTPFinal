"""
/app/controllers/product_payment_controller.py
Un solo precio base por producto, cargado con un método sin recargo.
El precio final para cada método se calcula: base * (1 + overload).
"""
import sqlite3

from app.controllers.common_controller import conflict, invalid, not_found, optional_text, transaction
from app.models.payment_method_model import PaymentMethodModel
from app.models.product_model import ProductModel
from app.models.product_payment_model import ProductPaymentModel

class ProductPaymentController:

    @staticmethod
    def _price(value) -> float:
        try:
            price = round(float(value), 2)
        except (TypeError, ValueError):
            raise invalid("'price' debe ser un número")
        if price < 0.01:
            raise invalid("'price' debe ser al menos 0.01")
        return price

    @staticmethod
    def _base_method(db: sqlite3.Connection, method_id: int) -> sqlite3.Row:
        method = PaymentMethodModel.get_by_id(db, method_id)
        if method is None:
            raise not_found("Método de pago", method_id)
        if method["overload"] > 0:
            raise conflict("El precio base se carga con un método sin recargo "
                           "(Efectivo, Transferencia o QR); los demás se calculan")
        return method

    @staticmethod
    def _row(db: sqlite3.Connection, product_payment_id: int) -> sqlite3.Row:
        row = ProductPaymentModel.get_by_id(db, product_payment_id)
        if row is None:
            raise not_found("Precio", product_payment_id)
        return row

    @staticmethod
    def get_all(db: sqlite3.Connection) -> list[dict]:
        return [dict(r) for r in ProductPaymentModel.get_all(db)]

    @staticmethod
    def get(db: sqlite3.Connection, product_payment_id: int) -> dict:
        return dict(ProductPaymentController._row(db, product_payment_id))

    @staticmethod
    def create(db: sqlite3.Connection, data: dict) -> dict:
        product_id = data.get("product_id")
        if ProductModel.get_by_id(db, product_id) is None:
            raise not_found("Producto", product_id)
        ProductPaymentController._base_method(db, data.get("payment_method_id"))
        if ProductPaymentModel.get_by_product(db, product_id) is not None:
            raise conflict("El producto ya tiene precio base: editá el existente")
        clean = {
            "product_id": product_id,
            "payment_method_id": data["payment_method_id"],
            "price": ProductPaymentController._price(data.get("price")),
            "currency": optional_text(data.get("currency"), "currency") or "Pesos",
        }
        with transaction(db):
            new_id = ProductPaymentModel.create(db, clean)
        return ProductPaymentController.get(db, new_id)

    @staticmethod
    def update(db: sqlite3.Connection, product_payment_id: int, data: dict) -> dict:
        current = ProductPaymentController._row(db, product_payment_id)
        method_id = data.get("payment_method_id", current["payment_method_id"])
        ProductPaymentController._base_method(db, method_id)
        clean = {
            "product_id": current["product_id"],   # un precio no se mueve de producto
            "payment_method_id": method_id,
            "price": ProductPaymentController._price(data.get("price", current["price"])),
            "currency": optional_text(data.get("currency"), "currency") or current["currency"],
        }
        with transaction(db):   # los pedidos viejos no cambian: guardan su propia foto de precio
            ProductPaymentModel.update(db, product_payment_id, clean)
        return ProductPaymentController.get(db, product_payment_id)

    @staticmethod
    def delete(db: sqlite3.Connection, product_payment_id: int) -> dict:
        deleted = ProductPaymentController.get(db, product_payment_id)
        with transaction(db):
            ProductPaymentModel.delete(db, product_payment_id)
        return deleted

    @staticmethod
    def price_list(db: sqlite3.Connection, product_id: int) -> dict:
        """Precio final del producto para cada método de pago (solo lectura)."""
        product = ProductModel.get_by_id(db, product_id)
        if product is None:
            raise not_found("Producto", product_id)
        base = ProductPaymentModel.get_by_product(db, product_id)
        if base is None:
            raise conflict(f"'{product['name']}' no tiene precio base cargado")
        return {
            "product_id": product_id,
            "name": product["name"],
            "base_price": base["price"],
            "currency": base["currency"],
            "prices": [
                {
                    "payment_method_id": m["payment_method_id"],
                    "method_name": m["method_name"],
                    "overload": m["overload"],
                    "final_price": round(base["price"] * (1 + m["overload"]), 2),
                }
                for m in PaymentMethodModel.get_all(db)
            ],
        }