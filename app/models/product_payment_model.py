"""
/app/models/product_payment_model.py
"""

import sqlite3
from typing import Optional

"""
CREATE TABLE IF NOT EXISTS product_payment (
    product_payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    payment_method_id INTEGER NOT NULL,
    price DECIMAL(10, 2) NOT NULL DEFAULT 0.01,
    currency TEXT NULL DEFAULT "Pesos");
"""
        
# class ProductPaymentBase(BaseModel):
#   product_id: int = Field(..., ge=1, example=1)
#   payment_method_id: int = Field(..., ge=1, example=1)
#   price: float = Field(..., ge=0.01, example=10.99)
#   currency: str = Field(..., min_length=1, max_length=100, example="Pesos")

class ProductPaymentModel:

    # esta funcion es para obtener todos los productos de la base de datos, se va a usar en el endpoint GET /products
    @staticmethod
    def get_all(conn: sqlite3.Connection) -> list[sqlite3.Row]:
        return conn.execute("""
            SELECT product_payment_id, product_id, payment_method_id, price, currency
            FROM product_payment
            ORDER BY product_payment_id;""").fetchall()

    @staticmethod
    def get_by_id(conn: sqlite3.Connection, product_payment_id: int) -> Optional[sqlite3.Row]:
        return conn.execute("""
            SELECT product_payment_id, product_id, payment_method_id, price, currency
            FROM product_payment
            WHERE product_payment_id = ?;""", (product_payment_id,)).fetchone()

    @staticmethod
    def get_by_product_and_payment(conn: sqlite3.Connection, product_id: int, payment_method_id: int) -> Optional[sqlite3.Row]:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT product_payment_id, product_id, payment_method_id, price, currency
            FROM product_payment
            WHERE product_id = ? AND payment_method_id = ?;""", (product_id, payment_method_id))
        return cursor.fetchone()

    @staticmethod
    def create(conn: sqlite3.Connection, product_payment_data: dict) -> int:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO product_payment (product_id, payment_method_id, price, currency)
            VALUES (?, ?, ?, ?);""", (
                product_payment_data["product_id"],
                product_payment_data["payment_method_id"],
                product_payment_data["price"],
                product_payment_data["currency"]))
        return cursor.lastrowid

    @staticmethod
    def update(conn: sqlite3.Connection, product_payment_id: int, product_payment_data: dict) -> bool:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE product_payment
            SET product_id = ?, payment_method_id = ?, price = ?, currency = ?
            WHERE product_payment_id = ?;""", (
                product_payment_data["product_id"],
                product_payment_data["payment_method_id"],
                product_payment_data["price"],
                product_payment_data["currency"],
                product_payment_id))
        return cursor.rowcount > 0

    @staticmethod
    def delete(conn: sqlite3.Connection, product_payment_id: int) -> bool:
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM product_payment 
            WHERE product_payment_id = ?;""", (product_payment_id,))
        return cursor.rowcount > 0

    @staticmethod
    def get_by_product(conn: sqlite3.Connection, product_id: int) -> Optional[sqlite3.Row]:
        return conn.execute("""
            SELECT product_payment_id, product_id, payment_method_id, price, currency
            FROM product_payment
            WHERE product_id = ?
            ORDER BY product_payment_id LIMIT 1;""", (product_id,)).fetchone()

    @staticmethod
    def delete_by_product(conn: sqlite3.Connection, product_id: int) -> None:
        conn.execute("DELETE FROM product_payment WHERE product_id = ?;", (product_id,))

    @staticmethod
    def count_by_method(conn: sqlite3.Connection, payment_method_id: int) -> int:
        return conn.execute(
            "SELECT COUNT(*) AS n FROM product_payment WHERE payment_method_id = ?;",
            (payment_method_id,)).fetchone()["n"]