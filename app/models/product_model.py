"""
/app/models/product_model.py
Acceso a datos de la tabla product. Solo SQL: las reglas viven en ProductController.
"""
import sqlite3
from typing import Optional

# Tabla (ver database.py):
#   product_id INTEGER PRIMARY KEY AUTOINCREMENT,
#   name TEXT NOT NULL, description TEXT NOT NULL,
#   ingredients TEXT NULL, taste TEXT NULL, texture TEXT NULL,
#   size TEXT NOT NULL, product_category TEXT NOT NULL,
#   product_subcategory TEXT NULL, product_group TEXT NULL, product_subgroup TEXT NULL,
#   stock INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0),
#   reserved_stock INTEGER NOT NULL DEFAULT 0 CHECK (reserved_stock >= 0)

COLUMNS = """product_id, name, description, ingredients, taste, texture, size,
             product_category, product_subcategory, product_group, product_subgroup,
             stock, reserved_stock"""


class ProductModel:

    # Todos los productos (GET /product)
    @staticmethod
    def get_all(conn: sqlite3.Connection) -> list[sqlite3.Row]:
        return conn.execute(f"SELECT {COLUMNS} FROM product ORDER BY product_id;").fetchall()

    # Un producto por id
    @staticmethod
    def get_by_id(conn: sqlite3.Connection, product_id: int) -> Optional[sqlite3.Row]:
        return conn.execute(
            f"SELECT {COLUMNS} FROM product WHERE product_id = ?;", (product_id,)).fetchone()

    # ¿Existe otro producto con el mismo nombre y tamaño? (exclude_id sirve al editar)
    @staticmethod
    def exists_name_size(conn: sqlite3.Connection, name: str, size: str,
                         exclude_id: Optional[int] = None) -> bool:
        row = conn.execute(
            "SELECT 1 FROM product WHERE lower(name) = lower(?) AND lower(size) = lower(?) "
            "AND product_id != ?;", (name, size, exclude_id or 0)).fetchone()
        return row is not None

    # Crea un producto y devuelve su id. reserved_stock siempre arranca en 0.
    @staticmethod
    def create(conn: sqlite3.Connection, product_data: dict) -> int:
        cursor = conn.execute("""
            INSERT INTO product (
                name, description, ingredients, taste, texture,
                size, product_category, product_subcategory,
                product_group, product_subgroup, stock, reserved_stock)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""", (
                product_data["name"],
                product_data["description"],
                product_data.get("ingredients"),
                product_data.get("taste"),
                product_data.get("texture"),
                product_data["size"],
                product_data["product_category"],
                product_data.get("product_subcategory"),
                product_data.get("product_group"),
                product_data.get("product_subgroup"),
                product_data.get("stock", 0),
                0))
        return cursor.lastrowid

    # Actualiza los datos del producto. No toca stock ni reserved_stock.
    @staticmethod
    def update(conn: sqlite3.Connection, product_id: int, product_data: dict) -> bool:
        cursor = conn.execute("""
            UPDATE product
            SET name = ?, description = ?, ingredients = ?, taste = ?, texture = ?,
                size = ?, product_category = ?, product_subcategory = ?,
                product_group = ?, product_subgroup = ?
            WHERE product_id = ?;""", (
                product_data["name"],
                product_data["description"],
                product_data.get("ingredients"),
                product_data.get("taste"),
                product_data.get("texture"),
                product_data["size"],
                product_data["product_category"],
                product_data.get("product_subcategory"),
                product_data.get("product_group"),
                product_data.get("product_subgroup"),
                product_id))
        return cursor.rowcount > 0

    # Reserva unidades sin descontar el stock físico (solo si hay disponible).
    @staticmethod
    def reserve_stock(conn: sqlite3.Connection, product_id: int, quantity: int) -> bool:
        if quantity <= 0:
            return False
        cursor = conn.execute("""
            UPDATE product
            SET reserved_stock = reserved_stock + ?
            WHERE product_id = ? AND (stock - reserved_stock) >= ?;""",
            (quantity, product_id, quantity))
        return cursor.rowcount > 0

    # Confirma la venta: descuenta stock físico y libera la reserva.
    @staticmethod
    def confirm_reserved_stock(conn: sqlite3.Connection, product_id: int, quantity: int) -> bool:
        if quantity <= 0:
            return False
        cursor = conn.execute("""
            UPDATE product
            SET stock = stock - ?, reserved_stock = reserved_stock - ?
            WHERE product_id = ? AND stock >= ? AND reserved_stock >= ?;""",
            (quantity, quantity, product_id, quantity, quantity))
        return cursor.rowcount > 0

    # Libera la reserva cuando se cancela un pedido pendiente.
    @staticmethod
    def release_reserved_stock(conn: sqlite3.Connection, product_id: int, quantity: int) -> bool:
        if quantity <= 0:
            return False
        cursor = conn.execute("""
            UPDATE product
            SET reserved_stock = reserved_stock - ?
            WHERE product_id = ? AND reserved_stock >= ?;""",
            (quantity, product_id, quantity))
        return cursor.rowcount > 0

    # Ingreso de producción o reposición de stock físico.
    @staticmethod
    def increase_stock(conn: sqlite3.Connection, product_id: int, quantity: int) -> bool:
        if quantity <= 0:
            return False
        cursor = conn.execute(
            "UPDATE product SET stock = stock + ? WHERE product_id = ?;", (quantity, product_id))
        return cursor.rowcount > 0

    # Elimina un producto. Devuelve True si existía.
    @staticmethod
    def delete(conn: sqlite3.Connection, product_id: int) -> bool:
        cursor = conn.execute("DELETE FROM product WHERE product_id = ?;", (product_id,))
        return cursor.rowcount > 0