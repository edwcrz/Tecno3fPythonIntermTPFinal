"""
/app/models/payment_method_model.py
"""
import sqlite3
from typing import Optional

"""
CREATE TABLE IF NOT EXISTS payment_method (
    payment_method_id INTEGER PRIMARY KEY AUTOINCREMENT,
    method_name TEXT NOT NULL DEFAULT "Efectivo",
    overload decimal(2, 2) NOT NULL DEFAULT 0.00,
    payment_term INTEGER NOT NULL DEFAULT 0,
    payment_category TEXT NULL,
    payment_subcategory TEXT NULL);
"""

# method_name: str = Field(..., min_length=1, max_length=100, example="Efectivo")
#   overload: float = Field(..., ge=0.00, example=0.00)
#   payment_term: int = Field(..., ge=0, example=0)
#   payment_category: Optional[str] = Field(None, max_length=100,example="Categoria 1")
#   payment_subcategory: Optional[str] = Field(None, max_length=100, example="Subcategoria 1")

class PaymentMethodModel:

    # esta funcion es para obtener todos los métodos de pago de la base de datos, 
    # se va a usar
    @staticmethod
    def get_all(conn: sqlite3.Connection) -> list[sqlite3.Row]:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT payment_method_id, method_name, overload, payment_term, payment_category, payment_subcategory 
            FROM payment_method;""")
        return cursor.fetchall()

    @staticmethod
    def get_by_id(conn: sqlite3.Connection, payment_method_id: int) -> Optional[sqlite3.Row]:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT payment_method_id, method_name, overload, payment_term, payment_category, payment_subcategory 
            FROM payment_method 
            WHERE payment_method_id = ?;""", (payment_method_id,))
        return cursor.fetchone()

    @staticmethod
    def create(conn: sqlite3.Connection, payment_method_data: dict) -> int:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO payment_method (method_name, overload, payment_term, payment_category, payment_subcategory)
            VALUES (?, ?, ?, ?, ?);""", (
                payment_method_data["method_name"],
                payment_method_data["overload"],
                payment_method_data["payment_term"],
                payment_method_data.get("payment_category"),
                payment_method_data.get("payment_subcategory")))
        return cursor.lastrowid

    @staticmethod
    def update(conn: sqlite3.Connection, payment_method_id: int, payment_method_data: dict) -> bool:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE payment_method
            SET method_name = ?, overload = ?, payment_term = ?, payment_category = ?, payment_subcategory = ?
            WHERE payment_method_id = ?;""", (
                payment_method_data["method_name"],
                payment_method_data["overload"],
                payment_method_data["payment_term"],
                payment_method_data.get("payment_category"),
                payment_method_data.get("payment_subcategory"),
                payment_method_id))
        return cursor.rowcount > 0

    @staticmethod
    def delete(conn: sqlite3.Connection, payment_method_id: int) -> bool:
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM payment_method 
            WHERE payment_method_id = ?;""", (payment_method_id,))
        return cursor.rowcount > 0
    
    @staticmethod
    def exists_name(conn: sqlite3.Connection, method_name: str, exclude_id: int | None = None) -> bool:
        row = conn.execute("""
            SELECT 1 
            FROM payment_method
            WHERE lower(method_name) = lower(?) AND payment_method_id != ?;""",
            (method_name, exclude_id or 0)).fetchone()
        return row is not None