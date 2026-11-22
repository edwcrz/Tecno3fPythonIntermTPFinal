"""
/app/models/order_detail_model.py
Acceso a datos de la tabla order_detail. Solo SQL: las reglas (precio, stock) viven en
OrderDetailController. Una línea no se edita: se quita y se vuelve a agregar.
"""
import sqlite3
from typing import Optional

# Tabla (ver database.py):
#   order_detail_id INTEGER PRIMARY KEY AUTOINCREMENT,
#   order_id INTEGER NOT NULL (FK a orders, ON DELETE CASCADE),
#   product_id INTEGER NOT NULL (FK a product, ON DELETE RESTRICT),
#   quantity INTEGER NOT NULL CHECK (quantity > 0),
#   unit_price REAL NOT NULL CHECK (unit_price >= 0),   -- foto del precio con recargo
#   subtotal REAL NOT NULL CHECK (subtotal >= 0)        -- unit_price * quantity

COLUMNS = "order_detail_id, order_id, product_id, quantity, unit_price, subtotal"

class OrderDetailModel:

    # Todas las líneas (GET /order_detail)
    @staticmethod
    def get_all(conn: sqlite3.Connection) -> list[sqlite3.Row]:
        return conn.execute(
            f"SELECT {COLUMNS} FROM order_detail ORDER BY order_detail_id;").fetchall()

    # Una línea por id
    @staticmethod
    def get_by_id(conn: sqlite3.Connection, order_detail_id: int) -> Optional[sqlite3.Row]:
        return conn.execute(
            f"SELECT {COLUMNS} FROM order_detail WHERE order_detail_id = ?;",
            (order_detail_id,)).fetchone()

    # Líneas de un pedido
    @staticmethod
    def get_by_order_id(conn: sqlite3.Connection, order_id: int) -> list[sqlite3.Row]:
        return conn.execute(
            f"SELECT {COLUMNS} FROM order_detail WHERE order_id = ? ORDER BY order_detail_id;",
            (order_id,)).fetchall()

    # Alias: los controllers usan este nombre
    @staticmethod
    def get_by_order(conn: sqlite3.Connection, order_id: int) -> list[sqlite3.Row]:
        return OrderDetailModel.get_by_order_id(conn, order_id)

    # Cantidad de líneas que usan un producto (para no borrar productos con historial)
    @staticmethod
    def count_by_product(conn: sqlite3.Connection, product_id: int) -> int:
        return conn.execute(
            "SELECT COUNT(*) AS n FROM order_detail WHERE product_id = ?;",
            (product_id,)).fetchone()["n"]

    # Crea una línea y devuelve su id. Recibe el dict que arma el controller.
    @staticmethod
    def create(conn: sqlite3.Connection, order_detail_data: dict) -> int:
        cursor = conn.execute("""
            INSERT INTO order_detail (order_id, product_id, quantity, unit_price, subtotal)
            VALUES (?, ?, ?, ?, ?);""", (
                order_detail_data["order_id"],
                order_detail_data["product_id"],
                order_detail_data["quantity"],
                order_detail_data["unit_price"],
                order_detail_data["subtotal"]))
        return cursor.lastrowid

    # Elimina una línea. Devuelve True si existía.
    # El controller libera la reserva de stock antes de llamarlo.
    @staticmethod
    def delete(conn: sqlite3.Connection, order_detail_id: int) -> bool:
        cursor = conn.execute(
            "DELETE FROM order_detail WHERE order_detail_id = ?;", (order_detail_id,))
        return cursor.rowcount > 0