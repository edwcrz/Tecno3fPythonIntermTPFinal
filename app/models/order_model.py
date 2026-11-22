"""
/app/models/order_model.py
Acceso a datos de la tabla orders. Solo SQL: las reglas viven en OrderController.
"""
import sqlite3
from typing import Optional

# Tabla (ver database.py):
#   order_id INTEGER PRIMARY KEY AUTOINCREMENT,
#   customer_id INTEGER NOT NULL (FK a customer),
#   date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
#   state TEXT NOT NULL DEFAULT 'pending' CHECK (pending | confirmed | cancelled),
#   communication TEXT NULL,
#   payment_method_id INTEGER NOT NULL (FK a payment_method),
#   total REAL NOT NULL DEFAULT 0

COLUMNS = "order_id, customer_id, date, state, communication, payment_method_id, total"


class OrderModel:

    # Todos los pedidos, el más nuevo primero (GET /order)
    @staticmethod
    def get_all(conn: sqlite3.Connection) -> list[sqlite3.Row]:
        return conn.execute(f"SELECT {COLUMNS} FROM orders ORDER BY order_id DESC;").fetchall()

    # Un pedido por id
    @staticmethod
    def get_by_id(conn: sqlite3.Connection, order_id: int) -> Optional[sqlite3.Row]:
        return conn.execute(
            f"SELECT {COLUMNS} FROM orders WHERE order_id = ?;", (order_id,)).fetchone()

    # Crea un pedido 'pending' con total 0 (fecha y estado salen de los defaults de la tabla).
    # El total lo calcula update_total cuando se cargan las líneas.
    @staticmethod
    def create(conn: sqlite3.Connection, customer_id: int, payment_method_id: int,
               communication: Optional[str]) -> int:
        cursor = conn.execute("""
            INSERT INTO orders (customer_id, communication, payment_method_id)
            VALUES (?, ?, ?);""", (customer_id, communication, payment_method_id))
        return cursor.lastrowid

    # Cambia solo el estado. La validación de la transición la hace OrderController.
    @staticmethod
    def update_state(conn: sqlite3.Connection, order_id: int, state: str) -> bool:
        cursor = conn.execute("UPDATE orders SET state = ? WHERE order_id = ?;", (state, order_id))
        return cursor.rowcount > 0

    # Recalcula el total sumando los subtotales de sus líneas.
    @staticmethod
    def update_total(conn: sqlite3.Connection, order_id: int) -> None:
        conn.execute("""
            UPDATE orders
            SET total = COALESCE((SELECT SUM(subtotal) FROM order_detail WHERE order_id = ?), 0)
            WHERE order_id = ?;""", (order_id, order_id))

    # Cantidad de pedidos de un cliente (para no borrar clientes con historial)
    @staticmethod
    def count_by_customer(conn: sqlite3.Connection, customer_id: int) -> int:
        return conn.execute(
            "SELECT COUNT(*) AS n FROM orders WHERE customer_id = ?;",
            (customer_id,)).fetchone()["n"]

    # Pedidos pendientes de un cliente
    @staticmethod
    def count_pending_by_customer(conn: sqlite3.Connection, customer_id: int) -> int:
        return conn.execute(
            "SELECT COUNT(*) AS n FROM orders WHERE customer_id = ? AND state = 'pending';",
            (customer_id,)).fetchone()["n"]

    # Método de pago de un pedido (para leer su recargo). Se usa desde los controllers de pedido.
    @staticmethod
    def get_payment_method(conn: sqlite3.Connection, payment_method_id: int) -> Optional[sqlite3.Row]:
        return conn.execute(
            "SELECT payment_method_id, method_name, overload FROM payment_method "
            "WHERE payment_method_id = ?;", (payment_method_id,)).fetchone()

    # Precio base del producto: el de product_payment cargado con un método sin recargo.
    @staticmethod
    def get_base_price(conn: sqlite3.Connection, product_id: int) -> Optional[float]:
        row = conn.execute("""
            SELECT pp.price
            FROM product_payment pp
            JOIN payment_method pm ON pm.payment_method_id = pp.payment_method_id
            WHERE pp.product_id = ? AND pm.overload = 0
            ORDER BY pp.product_payment_id LIMIT 1;""", (product_id,)).fetchone()
        return row["price"] if row else None