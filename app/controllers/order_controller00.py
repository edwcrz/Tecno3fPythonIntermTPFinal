### order_controller

"""
No debe ejecutar SQL directamente: para eso utiliza los Models. 
Su responsabilidad es aplicar las reglas comerciales, controlar el stock y administrar las transacciones.
"""

"""
Una orden nueva se crea en estado pending.
Al crearla, se reserva el stock, pero no se descuenta el stock físico.
Una orden pendiente puede modificarse o cancelarse.
Al confirmar la venta, pasa a sold, se descuenta el stock físico y se libera la reserva.
Una orden vendida no se puede modificar ni eliminar mediante las operaciones normales.
Se utiliza un único payment_method_id para toda la orden.
El precio de cada producto se obtiene de product_payment.price. No se vuelve a aplicar overload, porque ya está incluido en ese precio.
La dirección que se guarda es la dirección de entrega de esa orden, no una referencia a la agenda de domicilios del cliente.

El Controller va a coordinar las operaciones y las transacciones. Los modelos siguen siendo responsables exclusivamente de ejecutar SQL.

Se usan los siguientes métodos:
OrdersModel.create, get_all, get_by_id, update y delete.
OrderDetailModel.create, get_by_order_id y delete_by_order_id.
ProductModel.get_by_id, reserve_stock, confirm_reserved_stock y release_reserved_stock.
ProductPaymentModel.get_by_product_and_payment.
CustomerModel.get_by_id.
PaymentMethodModel.get_by_id.
"""
import sqlite3
from contextlib import contextmanager

from app.models.order_model import OrderModel
from models.order_detail_model import OrderDetailModel
from models.product_model import ProductModel
from models.product_payment_model import ProductPaymentModel
from models.payment_method_model import PaymentMethodModel
from models.customer_model import CustomerModel

class OrderController:

# ejecuto transacciones atómicas
    """
    Ejecuta todas las operaciones dentro de una única transacción.
    Si cualquier operación falla, realiza rollback.
    """
    @staticmethod
    @contextmanager
    def transaction(conn: sqlite3.Connection):
        if conn.in_transaction:
            raise RuntimeError("La conexión ya tiene una transacción activa.")
        conn.execute("BEGIN IMMEDIATE")

        try:
            yield
            conn.commit()
        except Exception:
            conn.rollback()
            raise

# realizo validaciones de cliente, de métodos de pago, de direcciones de entrega, de cantidad

    @staticmethod
    def validate_customer(conn, customer_id) -> str:
        customer = CustomerModel.get_by_id(conn, customer_id)
        if customer is None:
            raise ValueError(f"No existe el cliente con ID {customer_id}.")
        return customer

    @staticmethod
    def validate_payment_method(conn, payment_method_id) -> str:
        payment_method = PaymentMethodModel.get_by_id(conn, payment_method_id)
        if payment_method is None:
            raise ValueError(f"No existe el medio de pago con ID {payment_method_id}.")
        return payment_method

    @staticmethod
    def validate_delivery_address(order_data):
        address = order_data("address")
        if not isinstance(address, str) or not address.strip():
            raise ValueError("La dirección de entrega es obligatoria.")

    @staticmethod
    def validate_quantity(quantity):
        if isinstance(quantity, bool) or not isinstance(quantity, int):
            raise ValueError("La cantidad debe ser un número entero.")
        if quantity <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

    @staticmethod
    def get_pending_order(conn: sqlite3.Connection, order_id: int ) -> sqlite3.Row:
        order = OrderModel.get_by_id(conn, order_id)
        if order is None:
            raise ValueError(f"No existe la orden con ID {order_id}.")
        if order["state"] != "pending":
            raise ValueError("La operación solamente está permitida para órdenes pendientes.")
        return order

    # ---------------------------------------------------------
    # PREPARACIÓN DE DETALLES
    # ---------------------------------------------------------

    """
    Valida productos y cantidades.
    Obtiene el precio correspondiente al medio de pago.
    No aplica overload: ya está incluido en product_payment.price.
    """

    @staticmethod
    def prepare_details(conn: sqlite3.Connection, details: list[dict], payment_method_id: int) -> tuple[list[dict], dict[int, int], str]:
        if not details:
            raise ValueError("La orden debe contener al menos un producto.")
        prepared_details: list[dict] = []
        quantities_by_product: dict[int, int] = {}
        currencies: set[str] = set()
        for detail in details:
            product_id = detail.get("product_id")
            quantity = detail.get("quantity")
            if product_id is None:
                raise ValueError("Falta product_id en un detalle.")
            OrderController.validate_quantity(quantity)
            product = ProductModel.get_by_id(conn, product_id)
            if product is None:
                raise ValueError(f"No existe el producto con ID {product_id}.")
            product_payment = (
                ProductPaymentModel.get_by_product_and_payment(conn, product_id, payment_method_id))
            if product_payment is None:
                raise ValueError(f"El producto {product_id} no tiene un precio configurado para el medio de pago {payment_method_id}.")
            unit_price = float(product_payment["price"])
            if unit_price < 0:
                raise ValueError(f"El producto {product_id} tiene un precio inválido.")
            currency = product_payment["currency"] or "Pesos"
            currencies.add(currency)
            prepared_details.append({
                "product_id": product_id,
                "quantity": quantity,
                "unit_price": unit_price})
            quantities_by_product[product_id] = (
                quantities_by_product.get(product_id, 0) + quantity)
        if len(currencies) > 1:
            raise ValueError("Todos los productos de una orden deben utilizar la misma moneda.")
        currency = next(iter(currencies), "Pesos")
        return prepared_details, quantities_by_product, currency

    # ---------------------------------------------------------
    # GESTIÓN DE STOCK
    # ---------------------------------------------------------

    @staticmethod
    def reserve_stock(conn: sqlite3.Connection, quantities_by_product: dict[int, int] = {}):
        for product_id, quantity in quantities_by_product.items():
            reserved = ProductModel.reserve_stock(conn, product_id, quantity)
            if not reserved:
                raise ValueError(f"Stock insuficiente para reservar el producto {product_id}.")

    @staticmethod
    def release_stock(conn: sqlite3.Connection, quantities_by_product: dict[int, int] = {}):
        for product_id, quantity in quantities_by_product.items():
            released = ProductModel.release_reserved_stock(conn, product_id, quantity)
            if not released:
                raise ValueError(f"No se pudo liberar la reserva del producto {product_id}.")

    @staticmethod
    def consume_reserved_stock(conn: sqlite3.Connection, quantities_by_product: dict[int, int] = {}):
        for product_id, quantity in quantities_by_product.items():
            consumed = ProductModel.confirm_reserved_stock(conn, product_id, quantity)
            if not consumed:
                raise ValueError(f"No se pudo confirmar el stock reservado del producto {product_id}.")

    # ---------------------------------------------------------
    # DETALLES DE LA ORDEN
    # ---------------------------------------------------------

    @staticmethod
    def insert_details(conn: sqlite3.Connection, order_id: int, details):
        for detail in details:
            OrderDetailModel.create(conn, {
                "order_id": order_id,
                "product_id": detail["product_id"],
                "quantity": detail["quantity"],
                "unit_price": detail["unit_price"]})

    @staticmethod
    def get_quantities_from_order(conn: sqlite3.Connection, order_id: int) -> int:
        details = OrderDetailModel.get_by_order_id(conn, order_id: int)
        quantities = {}
        for detail in details:
            product_id = detail["product_id"]
            quantity = detail["quantity"]
            quantities[product_id] = (quantities.get(product_id, 0) + quantity)
        return quantities

    # ---------------------------------------------------------
    # CREAR ORDEN
    # ---------------------------------------------------------

    """
    Crea una orden pendiente y reserva el stock.
    El stock físico no se descuenta todavía.
    """
    @staticmethod
    def create_order( conn: sqlite3.Connection, order_data: dict, details: list) -> int:
        with OrderController.transaction(conn):
            customer_id = order_data["customer_id"]
            payment_method_id = order_data["payment_method_id"]
            OrderController.validate_customer(conn, customer_id)
            OrderController.validate_payment_method(conn, payment_method_id)
            OrderController.validate_delivery_address(order_data)
            prepared_details, quantities, currency = (OrderController.prepare_details( conn, details, payment_method_id))
            # Reserva de stock físico disponible.
            OrderController.reserve_stock(conn, quantities)
            # La orden siempre se crea como pending.
            new_order_data = {
                "customer_id": customer_id,
                "payment_method_id": payment_method_id,
                "state": "pending",
                "communication": order_data.get("communication"),

                "delivery_address": order_data["delivery_address"],
                "delivery_locality": order_data.get("delivery_locality"),
                "delivery_province": order_data.get("delivery_province"),
                "delivery_country": order_data.get("delivery_country"),
                "delivery_postal_code": order_data.get("delivery_postal_code"),
                "delivery_notes": order_data.get("delivery_notes"),

                "recipient_name": order_data.get("recipient_name"),
                "recipient_phone": order_data.get("recipient_phone"),
                "is_gift": int(bool(order_data.get("is_gift", False))),
                "gift_message": order_data.get("gift_message"),

                "currency": currency}
            order_id = OrderModel.create(conn, new_order_data)
            OrderController.insert_details(conn, order_id, prepared_details)
            return order_id

    # ---------------------------------------------------------
    # MODIFICAR ORDEN PENDIENTE
    # ---------------------------------------------------------

    """
    Reemplaza los datos y detalles de una orden pendiente.
    Libera las reservas anteriores y reserva las nuevas.
    Todo se ejecuta en una sola transacción.
    """

    @staticmethod
    def update_order(conn: sqlite3.Connection, order_id: int, order_data: dict, details: list) -> bool:
        with OrderController.transaction(conn):
            OrderController.get_pending_order(conn, order_id)
            customer_id = order_data["customer_id"]
            payment_method_id = order_data["payment_method_id"]
            OrderController.validate_customer(conn, customer_id)
            OrderController.validate_payment_method(conn, payment_method_id)
            OrderController.validate_delivery_address(order_data)
            # Recupera y libera las reservas anteriores.
            old_quantities = OrderController.get_quantities_from_order(conn, order_id)
            OrderController.release_stock(conn, old_quantities)
            # Prepara los nuevos detalles y precios.
            prepared_details, new_quantities, currency = (OrderController.prepare_details(conn, details, payment_method_id))
            # Reserva las nuevas cantidades.
            OrderController.reserve_stock(conn, new_quantities)
            # Actualiza los datos generales.
            updated_order_data = {
                "customer_id": customer_id,
                "payment_method_id": payment_method_id,
                "communication": order_data.get("communication"),

                "delivery_address": order_data["delivery_address"],
                "delivery_locality": order_data.get("delivery_locality"),
                "delivery_province": order_data.get("delivery_province"),
                "delivery_country": order_data.get("delivery_country"),
                "delivery_postal_code": order_data.get("delivery_postal_code"),
                "delivery_notes": order_data.get("delivery_notes"),

                "recipient_name": order_data.get("recipient_name"),
                "recipient_phone": order_data.get("recipient_phone"),
                "is_gift": int(bool(order_data.get("is_gift", False))),
                "gift_message": order_data.get("gift_message"),

                "currency": currency}
            updated = OrderModel.update(conn, order_id, updated_order_data)
            if not updated:
                raise ValueError(f"No se pudo actualizar la orden {order_id}.")
            # Reemplaza los detalles anteriores.
            OrderDetailModel.delete_by_order_id(conn, order_id)
            OrderController.insert_details(conn, order_id, prepared_details)
            return True

    # ---------------------------------------------------------
    # CONFIRMAR VENTA
    # ---------------------------------------------------------

	"""
    Confirma la venta.
    Convierte las reservas en descuentos de stock físico.
    Cambia el estado a sold.
    """
    @staticmethod
    def confirm_order(conn: sqlite3.Connection, order_id: int) -> bool:
        with OrderController.transaction(conn):
            OrderController.get_pending_order(conn, order_id)
            quantities = OrderController.get_quantities_from_order(conn, order_id)
            if not quantities:
                raise ValueError("No se puede confirmar una orden sin detalles.")
            OrderController.consume_reserved_stock(conn, quantities)
            updated = OrderModel.update(conn, order_id, {"state": "sold"})
            if not updated:
                raise ValueError(f"No se pudo confirmar la orden {order_id}.")
            return True

    # ---------------------------------------------------------
    # CANCELAR ORDEN
    # ---------------------------------------------------------

    """
    Cancela una orden pendiente y libera sus reservas.
    No modifica el stock físico.
    """
    @staticmethod
    def cancel_order(conn: sqlite3.Connection, order_id: int) -> bool:
        with OrderController.transaction(conn):
            OrderController.get_pending_order(conn, order_id)
            quantities = OrderController.get_quantities_from_order(conn, order_id)
            OrderController.release_stock(conn, quantities)
            updated = OrderModel.update(conn, order_id, {"state": "cancelled"})
            if not updated:
                raise ValueError(f"No se pudo cancelar la orden {order_id}.")
            return True

    # ---------------------------------------------------------
    # ELIMINAR ORDEN
    # ---------------------------------------------------------

	"""
    Elimina una orden que no fue vendida.
    Si está pending, primero libera las reservas.
    Una orden sold no se puede eliminar.
    """

    @staticmethod
    def delete_order(conn: sqlite3.Connection, order_id: int) -> bool:
        with OrderController.transaction(conn):
            order = OrderModel.get_by_id(conn, order_id)
            if order is None:
                raise ValueError(f"No existe la orden con ID {order_id}.")
            if order["state"] == "sold":
                raise ValueError("No se puede eliminar una orden vendida.")
            if order["state"] == "pending":
                quantities = OrderController.get_quantities_from_order(conn, order_id)
                OrderController.release_stock(conn, quantities)
            deleted = OrderModel.delete(conn, order_id)
            if not deleted:
                raise ValueError(f"No se pudo eliminar la orden {order_id}.")
            return True

    # ---------------------------------------------------------
    # CONSULTAS
    # ---------------------------------------------------------

    @staticmethod
    def get_order_by_id(conn: sqlite3.Connection, order_id: int) -> Optional[dict[str, any]]:
        order = OrderModel.get_by_id(conn, order_id)
        if order is None:
            return None
        order_result = dict(order)
        details = OrderDetailModel.get_by_order_id(conn, order_id)
        order_result["details"] = [dict(detail) for detail in details]
        order_result["total"] = sum(detail["quantity"] * detail["unit_price"]for detail in details)
        return order_result

    @staticmethod
    def get_all_orders(conn: sqlite3.Connection) -> list[dict[str, any]]:
        orders = OrderModel.get_all(conn)
        result = list[dict[str, any]] = []
        for order in orders:
            order_result = OrderController.get_order_by_id(conn, order["order_id"])
            if order_result is not None:
                result.append(order_result)
        return result