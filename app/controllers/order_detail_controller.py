"""
/app/controllers/order_detail_controller.py
Una línea = precio con recargo (foto) + reserva de stock.
unit_price = precio base * (1 + overload) ; subtotal = unit_price * quantity
"""
import sqlite3

from app.controllers.common_controller import conflict, not_found, positive_int, transaction
from app.models.order_model import OrderModel
from app.models.order_detail_model import OrderDetailModel
from app.models.product_model import ProductModel


class OrderDetailController:

    # Lógica interna: NO hace commit, la transacción la maneja quien llama.
    @staticmethod
    def add_line(db: sqlite3.Connection, order_id: int, product_id: int,
                 quantity: int, overload: float) -> None:
        quantity = positive_int(quantity, "quantity")

        product = ProductModel.get_by_id(db, product_id)
        if product is None:
            raise not_found("Producto", product_id)

        base_price = OrderModel.get_base_price(db, product_id)
        if base_price is None:
            raise conflict(f"'{product['name']}' no tiene precio base cargado")

        # Sin stock disponible (stock - reservado) no se vende.
        if not ProductModel.reserve_stock(db, product_id, quantity):
            available = product["stock"] - product["reserved_stock"]
            raise conflict(f"Stock insuficiente de '{product['name']}': "
                           f"pedido {quantity}, disponible {available}")

        unit_price = round(base_price * (1 + overload), 2)
        subtotal = round(unit_price * quantity, 2)
        OrderDetailModel.create(db, {
            "order_id": order_id,
            "product_id": product_id,
            "quantity": quantity,
            "unit_price": unit_price,
            "subtotal": subtotal,})

    @staticmethod
    def _pending_order(db: sqlite3.Connection, order_id: int) -> sqlite3.Row:
        order = OrderModel.get_by_id(db, order_id)
        if order is None:
            raise not_found("Pedido", order_id)
        if order["state"] != "pending":
            raise conflict(f"El pedido está '{order['state']}': solo se modifica si está 'pending'")
        return order

    @staticmethod
    def list_by_order(db: sqlite3.Connection, order_id: int) -> list[dict]:
        if OrderModel.get_by_id(db, order_id) is None:
            raise not_found("Pedido", order_id)
        return [dict(r) for r in OrderDetailModel.get_by_order(db, order_id)]

    @staticmethod
    def get(db: sqlite3.Connection, order_detail_id: int) -> dict:
        row = OrderDetailModel.get_by_id(db, order_detail_id)
        if row is None:
            raise not_found("Línea", order_detail_id)
        return dict(row)

    @staticmethod
    def add_item(db: sqlite3.Connection, order_id: int, product_id: int, quantity: int) -> list[dict]:
        order = OrderDetailController._pending_order(db, order_id)
        method = OrderModel.get_payment_method(db, order["payment_method_id"])
        with transaction(db):
            OrderDetailController.add_line(db, order_id, product_id, quantity, method["overload"])
            OrderModel.update_total(db, order_id)
        return OrderDetailController.list_by_order(db, order_id)

    @staticmethod
    def remove_item(db: sqlite3.Connection, order_id: int, order_detail_id: int) -> list[dict]:
        OrderDetailController._pending_order(db, order_id)
        line = OrderDetailModel.get_by_id(db, order_detail_id)
        if line is None or line["order_id"] != order_id:
            raise not_found("Línea", f"{order_detail_id} del pedido {order_id}")
        if len(OrderDetailModel.get_by_order(db, order_id)) == 1:
            raise conflict("No se puede dejar el pedido vacío: cancelalo en su lugar")
        with transaction(db):
            ProductModel.release_reserved_stock(db, line["product_id"], line["quantity"])
            OrderDetailModel.delete(db, order_detail_id)
            OrderModel.update_total(db, order_id)
        return OrderDetailController.list_by_order(db, order_id)