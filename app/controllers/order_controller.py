"""
/app/controllers/order_controller.py
- Solo se vende a clientes con email y dirección registrados.
- Sin stock disponible no se vende.
- La dirección NO se copia al pedido: se lee del cliente al consultar.
- Estados: pending -> confirmed | cancelled (confirmed y cancelled son finales).
"""
import sqlite3
from typing import Optional

from app.controllers.common_controller import conflict, invalid, not_found, optional_text, positive_int, transaction
from app.controllers.customer_controller import CustomerController
from app.controllers.order_detail_controller import OrderDetailController
from app.models.order_model import OrderModel
from app.models.order_detail_model import OrderDetailModel
from app.models.product_model import ProductModel

VALID_TRANSITIONS = {
    "pending": {"confirmed", "cancelled"},
    "confirmed": set(),
    "cancelled": set(),
}


class OrderController:

    @staticmethod
    def _merge_items(items: list[dict]) -> dict[int, int]:
        """Valida cantidades y suma los productos repetidos."""
        if not items:
            raise invalid("El pedido debe tener al menos un producto")
        merged: dict[int, int] = {}
        for item in items:
            qty = positive_int(item.get("quantity"), "quantity")
            merged[item["product_id"]] = merged.get(item["product_id"], 0) + qty
        return merged

    @staticmethod
    def _present(db: sqlite3.Connection, order: sqlite3.Row) -> dict:
        data = dict(order)
        data["items"] = [dict(r) for r in OrderDetailModel.get_by_order(db, order["order_id"])]
        # Datos de entrega: se leen del cliente, no se guardan en el pedido.
        customer = CustomerController.get(db, order["customer_id"])
        data["customer"] = {k: customer[k] for k in ("customer_id", "name", "surname", "email", "phone")}
        data["delivery_addresses"] = customer["addresses"]
        return data

    @staticmethod
    def get_all(db: sqlite3.Connection) -> list[dict]:
        return [OrderController._present(db, o) for o in OrderModel.get_all(db)]

    @staticmethod
    def get(db: sqlite3.Connection, order_id: int) -> dict:
        order = OrderModel.get_by_id(db, order_id)
        if order is None:
            raise not_found("Pedido", order_id)
        return OrderController._present(db, order)

    @staticmethod
    def create(db: sqlite3.Connection, customer_id: int, payment_method_id: int,
               communication: Optional[str], items: list[dict]) -> dict:
        CustomerController.validate_can_buy(db, customer_id)

        method = OrderModel.get_payment_method(db, payment_method_id)
        if method is None:
            raise not_found("Método de pago", payment_method_id)

        merged = OrderController._merge_items(items)
        communication = optional_text(communication, "communication", 500)

        with transaction(db):   # si un ítem falla: sin pedido ni reservas a medias
            order_id = OrderModel.create(db, customer_id, payment_method_id, communication)
            for product_id, quantity in merged.items():
                OrderDetailController.add_line(db, order_id, product_id, quantity, method["overload"])
            OrderModel.update_total(db, order_id)
        return OrderController.get(db, order_id)

    @staticmethod
    def change_state(db: sqlite3.Connection, order_id: int, new_state: str) -> dict:
        order = OrderModel.get_by_id(db, order_id)
        if order is None:
            raise not_found("Pedido", order_id)
        if new_state not in VALID_TRANSITIONS:
            raise invalid(f"Estado inválido: {new_state}")
        if new_state not in VALID_TRANSITIONS[order["state"]]:
            raise conflict(f"No se puede pasar de '{order['state']}' a '{new_state}'")

        lines = OrderDetailModel.get_by_order(db, order_id)
        with transaction(db):
            for line in lines:
                if new_state == "confirmed":
                    ok = ProductModel.confirm_reserved_stock(db, line["product_id"], line["quantity"])
                else:
                    ok = ProductModel.release_reserved_stock(db, line["product_id"], line["quantity"])
                if not ok:
                    raise conflict(f"Inconsistencia de stock en el producto {line['product_id']}")
            OrderModel.update_state(db, order_id, new_state)
        return OrderController.get(db, order_id)