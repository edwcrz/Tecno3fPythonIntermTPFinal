"""
/app/controllers/payment_method_controller.py
Reglas: nombre único, overload entre 0 y 1 (0.10 = 10%), y un método con precios
cargados no puede pasar a tener recargo (los precios base viven en métodos sin recargo).
"""
import sqlite3

from app.controllers.common_controller import (conflict, invalid, not_found, non_negative_int, optional_text, required_text, transaction)
from app.models.payment_method_model import PaymentMethodModel
from app.models.product_payment_model import ProductPaymentModel

class PaymentMethodController:

    @staticmethod
    def _row(db: sqlite3.Connection, method_id: int) -> sqlite3.Row:
        row = PaymentMethodModel.get_by_id(db, method_id)
        if row is None:
            raise not_found("Método de pago", method_id)
        return row

    @staticmethod
    def _clean(db: sqlite3.Connection, data: dict, exclude_id: int | None = None) -> dict:
        name = required_text(data.get("method_name"), "method_name")
        if PaymentMethodModel.exists_name(db, name, exclude_id):
            raise conflict(f"Ya existe el método de pago '{name}'")
        try:
            overload = round(float(data.get("overload") or 0), 4)
        except (TypeError, ValueError):
            raise invalid("'overload' debe ser un número")
        if not 0 <= overload <= 1:
            raise invalid("'overload' debe estar entre 0 y 1 (0.10 = 10%)")
        return {
            "method_name": name,
            "overload": overload,
            "payment_term": non_negative_int(data.get("payment_term") or 0, "payment_term"),
            "payment_category": optional_text(data.get("payment_category"), "payment_category"),
            "payment_subcategory": optional_text(data.get("payment_subcategory"), "payment_subcategory"),
        }

    @staticmethod
    def get_all(db: sqlite3.Connection) -> list[dict]:
        return [dict(r) for r in PaymentMethodModel.get_all(db)]

    @staticmethod
    def get(db: sqlite3.Connection, method_id: int) -> dict:
        return dict(PaymentMethodController._row(db, method_id))

    @staticmethod
    def create(db: sqlite3.Connection, data: dict) -> dict:
        clean = PaymentMethodController._clean(db, data)
        with transaction(db):
            new_id = PaymentMethodModel.create(db, clean)
        return PaymentMethodController.get(db, new_id)

    @staticmethod
    def update(db: sqlite3.Connection, method_id: int, data: dict) -> dict:
        PaymentMethodController._row(db, method_id)
        clean = PaymentMethodController._clean(db, data, exclude_id=method_id)
        if clean["overload"] > 0 and ProductPaymentModel.count_by_method(db, method_id) > 0:
            raise conflict("Este método tiene precios base cargados: no puede tener recargo")
        with transaction(db):
            PaymentMethodModel.update(db, method_id, clean)
        return PaymentMethodController.get(db, method_id)

    @staticmethod
    def delete(db: sqlite3.Connection, method_id: int) -> dict:
        deleted = PaymentMethodController.get(db, method_id)
        with transaction(db):   # si hay pedidos o precios que lo usan, la FK lo rechaza con 409
            PaymentMethodModel.delete(db, method_id)
        return deleted