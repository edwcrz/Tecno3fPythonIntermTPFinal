# ProductModel

"""
/app/models/product_model.py
"""

import sqlite3
from typing import Optional

"""
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    ingredients TEXT NULL,
    taste TEXT NULL,
    texture TEXT NULL,
    size TEXT NOT NULL,
    product_category TEXT NOT NULL,
    product_subcategory TEXT NULL,
    product_group TEXT NULL,
    product_subgroup TEXT NULL,
    stock INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0),
    reserved_stock INTEGER NOT NULL DEFAULT 0 CHECK (reserved_stock >= 0));
"""

# name: str = Field(..., min_length=1, max_length=100, example="Product Name")
#   description: str = Field(..., min_length=1, max_length=100, example="Product Description")
#   ingredients: Optional[str] = Field(None, max_length=100, example="Product Ingredients")
#   taste: Optional[str] = Field(None, max_length=100, example="Product Taste")
#   texture: Optional[str] = Field(None, max_length=100, example="Product Texture")
#   size: str = Field(..., min_length=1, max_length=100, example="Product Size")
#   product_category: str = Field(..., min_length=1, max_length=100, example="Product Category")
#   product_subcategory: Optional[str] = Field(None, max_length=100, example="Product Subcategory")
#   product_group: Optional[str] = Field(None, max_length=100, example="Product Group")
#   product_subgroup: Optional[str] = Field(None, max_length=100, example="Product Subgroup")
#   stock : int = Field(..., ge=0, example=10)
#   reserved_stock : int = Field(..., ge=0, example=10)

class ProductModel:

    @staticmethod
    def exists_name_size(conn, name: str, size: str, exclude_id: int | None = None) -> bool:
        row = conn.execute(
            "SELECT 1 FROM product WHERE lower(name) = lower(?) AND lower(size) = lower(?) "
            "AND product_id != ?;", (name, size, exclude_id or 0)).fetchone()
        return row is not None

    # PaymentMethodModel
    @staticmethod
    def exists_name(conn, method_name: str, exclude_id: int | None = None) -> bool:
        row = conn.execute(
            "SELECT 1 FROM payment_method WHERE lower(method_name) = lower(?) "
            "AND payment_method_id != ?;", (method_name, exclude_id or 0)).fetchone()
        return row is not None

    # ProductPaymentModel
    @staticmethod
    def get_by_product(conn, product_id: int):
        return conn.execute("SELECT * FROM product_payment WHERE product_id = ?;", (product_id,)).fetchone()

    @staticmethod
    def delete_by_product(conn, product_id: int) -> None:
        conn.execute("DELETE FROM product_payment WHERE product_id = ?;", (product_id,))

    @staticmethod
    def count_by_method(conn, payment_method_id: int) -> int:
        return conn.execute("SELECT COUNT(*) AS n FROM product_payment WHERE payment_method_id = ?;",
                            (payment_method_id,)).fetchone()["n"]

    # CustomerModel
    @staticmethod
    def get_by_email(conn, email: str):
        return conn.execute("SELECT * FROM customer WHERE lower(email) = lower(?);", (email,)).fetchone()

    # CustomerAddressModel
    @staticmethod
    def get_by_customer(conn, customer_id: int):
        return conn.execute("SELECT * FROM customer_address WHERE customer_id = ? ORDER BY address_id;",
                            (customer_id,)).fetchall()

    @staticmethod
    def count_by_customer(conn, customer_id: int) -> int:
        return conn.execute("SELECT COUNT(*) AS n FROM customer_address WHERE customer_id = ?;",
                            (customer_id,)).fetchone()["n"]

    @staticmethod
    def delete_by_customer(conn, customer_id: int) -> None:
        conn.execute("DELETE FROM customer_address WHERE customer_id = ?;", (customer_id,))

    # OrderModel (agregar) y BORRAR get_customer y count_addresses, que ahora viven en CustomerController
    @staticmethod
    def count_by_customer(conn, customer_id: int) -> int:
        return conn.execute("SELECT COUNT(*) AS n FROM orders WHERE customer_id = ?;",
                            (customer_id,)).fetchone()["n"]

    @staticmethod
    def count_pending_by_customer(conn, customer_id: int) -> int:
        return conn.execute("SELECT COUNT(*) AS n FROM orders WHERE customer_id = ? AND state = 'pending';",
                            (customer_id,)).fetchone()["n"]

    # OrderDetailModel (agregar)
    @staticmethod
    def count_by_product(conn, product_id: int) -> int:
        return conn.execute("SELECT COUNT(*) AS n FROM order_detail WHERE product_id = ?;",
                            (product_id,)).fetchone()["n"]