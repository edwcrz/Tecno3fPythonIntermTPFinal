"""
/app/models/customer_model.py
Acceso a datos de la tabla customer. Solo SQL: las reglas viven en CustomerController.
"""
import sqlite3
from typing import Optional

# Tabla (ver database.py):
#   customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
#   name TEXT NOT NULL, nickname TEXT NULL, surname TEXT NULL,
#   email TEXT NULL, instagram TEXT NULL, phone TEXT NULL,
#   age TEXT NULL, gender TEXT NULL,
#   likes INTEGER NULL DEFAULT 0, notes TEXT NULL
#
# Los schemas de validación están en /app/views/customer_schema.py

COLUMNS = "customer_id, name, nickname, surname, email, instagram, phone, age, gender, likes, notes"

class CustomerModel:

    # Todos los clientes (GET /customer)
    @staticmethod
    def get_all(conn: sqlite3.Connection) -> list[sqlite3.Row]:
        return conn.execute(f"SELECT {COLUMNS} FROM customer ORDER BY customer_id;").fetchall()

    # Un cliente por id
    @staticmethod
    def get_by_id(conn: sqlite3.Connection, customer_id: int) -> Optional[sqlite3.Row]:
        return conn.execute(
            f"SELECT {COLUMNS} FROM customer WHERE customer_id = ?;", (customer_id,)).fetchone()

    # Un cliente por email (sin distinguir mayúsculas). Lo usa el controller para evitar duplicados.
    @staticmethod
    def get_by_email(conn: sqlite3.Connection, email: str) -> Optional[sqlite3.Row]:
        return conn.execute(
            f"SELECT {COLUMNS} FROM customer WHERE lower(email) = lower(?);", (email,)).fetchone()

    # Crea un cliente y devuelve su id (lastrowid = id del último registro insertado)
    @staticmethod
    def create(conn: sqlite3.Connection, customer_data: dict) -> int:
        cursor = conn.execute("""
            INSERT INTO customer (name, nickname, surname, email, instagram, phone, age, gender, likes, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""", (
                customer_data["name"],
                customer_data.get("nickname"),
                customer_data.get("surname"),
                customer_data.get("email"),
                customer_data.get("instagram"),
                customer_data.get("phone"),
                customer_data.get("age"),
                customer_data.get("gender"),
                customer_data.get("likes", 0),
                customer_data.get("notes")))
        return cursor.lastrowid

    # Actualiza un cliente. Devuelve True si existía.
    @staticmethod
    def update(conn: sqlite3.Connection, customer_id: int, customer_data: dict) -> bool:
        cursor = conn.execute("""
            UPDATE customer
            SET name = ?, nickname = ?, surname = ?, email = ?, instagram = ?,
                phone = ?, age = ?, gender = ?, likes = ?, notes = ?
            WHERE customer_id = ?;""", (
                customer_data["name"],
                customer_data.get("nickname"),
                customer_data.get("surname"),
                customer_data.get("email"),
                customer_data.get("instagram"),
                customer_data.get("phone"),
                customer_data.get("age"),
                customer_data.get("gender"),
                customer_data.get("likes", 0),
                customer_data.get("notes"),
                customer_id))
        return cursor.rowcount > 0

    # Elimina un cliente. Devuelve True si existía.
    # Con direcciones o pedidos la FK lo rechaza (RESTRICT); el controller lo previene antes.
    @staticmethod
    def delete(conn: sqlite3.Connection, customer_id: int) -> bool:
        cursor = conn.execute("DELETE FROM customer WHERE customer_id = ?;", (customer_id,))
        return cursor.rowcount > 0