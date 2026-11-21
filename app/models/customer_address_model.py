"""
/app/models/CustomerAddressModel
Acceso a datos de la tabla customer_address. Solo SQL: las reglas viven en CustomerAddressController.

"""

import sqlite3
from typing import Optional

"""
CREATE TABLE IF NOT EXISTS customer_address (
    address_id INTEGER PRIMARY KEY AUTOINCREMENT,
    address TEXT NOT NULL,
    locality TEXT NULL,
    province TEXT NULL,
    pais TEXT NULL,
    postal_code TEXT NULL,
    notes TEXT NULL,
    customer_id INTEGER NOT NULL,
"""

# class CustomerAddressBase(BaseModel):
#   address: str = Field(..., min_length=1, max_length=200, example="Customer Address")
#   locality: Optional[str] = Field(None, max_length=100, example="Customer Locality")
#   province: Optional[str] = Field(None, max_length=100, example="Customer Province")
#   pais: Optional[str] = Field(None, max_length=100, example="Customer Country")
#   postal_code: Optional[str] = Field(None, max_length=20, example="Customer Postal Code")
#   notes: Optional[str] = Field(None, max_length=200, example="Customer Notes")
#   customer_id: int = Field(..., example=1)

 # Tabla (ver database.py):
#   address_id INTEGER PRIMARY KEY AUTOINCREMENT,
#   address TEXT NOT NULL, locality TEXT NULL, province TEXT NULL,
#   pais TEXT NULL, postal_code TEXT NULL, notes TEXT NULL,
#   customer_id INTEGER NOT NULL (FK a customer, ON DELETE RESTRICT)

COLUMNS = "address_id, address, locality, province, pais, postal_code, notes, customer_id"

class CustomerAddressModel:

    # Todas las direcciones (GET /customer_address)
    @staticmethod
    def get_all(conn: sqlite3.Connection) -> list[sqlite3.Row]:
        return conn.execute(
            f"SELECT {COLUMNS} FROM customer_address ORDER BY address_id;").fetchall()

    # Una dirección por su id
    @staticmethod
    def get_by_id(conn: sqlite3.Connection, address_id: int) -> Optional[sqlite3.Row]:
        return conn.execute(
            f"SELECT {COLUMNS} FROM customer_address WHERE address_id = ?;", (address_id,)).fetchone()

    # Direcciones de un cliente
    @staticmethod
    def get_by_customer_id(conn: sqlite3.Connection, customer_id: int) -> list[sqlite3.Row]:
        return conn.execute(
            f"SELECT {COLUMNS} FROM customer_address WHERE customer_id = ? ORDER BY address_id;",
            (customer_id,)).fetchall()

    # Alias: los controllers usan este nombre
    @staticmethod
    def get_by_customer(conn: sqlite3.Connection, customer_id: int) -> list[sqlite3.Row]:
        return CustomerAddressModel.get_by_customer_id(conn, customer_id)

    # Cantidad de direcciones de un cliente
    @staticmethod
    def count_by_customer(conn: sqlite3.Connection, customer_id: int) -> int:
        return conn.execute(
            "SELECT COUNT(*) AS n FROM customer_address WHERE customer_id = ?;",
            (customer_id,)).fetchone()["n"]

    # Crea una dirección y devuelve su id
    @staticmethod
    def create(conn: sqlite3.Connection, customer_address_data: dict) -> int:
        cursor = conn.execute("""
            INSERT INTO customer_address (address, locality, province, pais, postal_code, notes, customer_id)
            VALUES (?, ?, ?, ?, ?, ?, ?);""", (
                customer_address_data["address"],
                customer_address_data.get("locality"),
                customer_address_data.get("province"),
                customer_address_data.get("pais"),
                customer_address_data.get("postal_code"),
                customer_address_data.get("notes"),
                customer_address_data["customer_id"]))
        return cursor.lastrowid

    # Actualiza una dirección. Devuelve True si existía.
    @staticmethod
    def update(conn: sqlite3.Connection, address_id: int, customer_address_data: dict) -> bool:
        cursor = conn.execute("""
            UPDATE customer_address
            SET address = ?, locality = ?, province = ?, pais = ?, postal_code = ?,
                notes = ?, customer_id = ?
            WHERE address_id = ?;""", (
                customer_address_data["address"],
                customer_address_data.get("locality"),
                customer_address_data.get("province"),
                customer_address_data.get("pais"),
                customer_address_data.get("postal_code"),
                customer_address_data.get("notes"),
                customer_address_data["customer_id"],
                address_id))
        return cursor.rowcount > 0

    # Elimina una dirección. Devuelve True si existía.
    @staticmethod
    def delete(conn: sqlite3.Connection, address_id: int) -> bool:
        cursor = conn.execute("DELETE FROM customer_address WHERE address_id = ?;", (address_id,))
        return cursor.rowcount > 0

    # Elimina todas las direcciones de un cliente (lo usa CustomerController.delete)
    @staticmethod
    def delete_by_customer(conn: sqlite3.Connection, customer_id: int) -> None:
        conn.execute("DELETE FROM customer_address WHERE customer_id = ?;", (customer_id,))