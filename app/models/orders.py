import sqlite3
from typing import Optional

"""
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    state TEXT NOT NULL DEFAULT 'pending',
    communication TEXT NULL,
    payment_method TEXT NOT NULL DEFAULT 'efectivo'
)"""

# class OrderBase(BaseModel):
#   customer_id: int = Field(..., example=1)
#   date: datetime = Field(..., example="2023-01-01 00:00:00")
#   state: str = Field(..., min_length=1, max_length=100, example="pending")
#   communication: Optional[str] = Field(None, max_length=200, example="Order Communication")
#   payment_methond: str = Field(..., min_length=1, max_length=100, example="efectivo")

class OrdersModel:

    @staticmethod
    # esta funcion es para obtener todas las ordenes de la base de datos, 
    # se va a usar en el endpoint GET /orders
    def get_all(conn: sqlite3.Connection) -> list[sqlite3.Row]:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT order_id, customer_id, date, state, communication, payment_method 
            FROM orders """)
        return cursor.fetchall()

    @staticmethod
    # esta funcion es para obtener una orden por su id de la base de datos, 
    # se va a usar en el endpoint GET /orders/{order_id}
    def get_by_id(conn: sqlite3.Connection, order_id: int) -> Optional[sqlite3.Row]:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT order_id, customer_id, date, state, communication, payment_method 
            FROM orders 
            WHERE order_id = ? """, (order_id,))
        return cursor.fetchone()        

    # esta funcion es para crear una orden en la base de datos, 
    # se va a usar en el endpoint POST /orders
    # va a recibir un diccionario con los datos de la orden, y va a devolver el id de la orden creada
    # para eso vamos a usar el metodo lastrowid del cursor, que devuelve el id del ultimo registro insertado
    @staticmethod
    def create(conn: sqlite3.Connection, order_data: dict) -> int:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO orders (customer_id, date, state, communication, payment_method)
            VALUES (?, ?, ?, ?, ?) """, (
                order_data["customer_id"],
                order_data["date"],
                order_data["state"],
                order_data.get("communication"),
                order_data["payment_method"]))
        return cursor.lastrowid

    # esta funcion es para actualizar una orden en la base de datos, se va a usar
    # va a recibir el id de la orden a actualizar y un diccionario con los nuevos datos
    @staticmethod
    def update(conn: sqlite3.Connection, order_id: int, order_data: dict) -> bool:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE orders
            SET customer_id = ?, date = ?, state = ?, communication = ?, payment_method = ?
            WHERE order_id = ? """, (
                order_data["customer_id"],
                order_data["date"],
                order_data["state"],
                order_data.get("communication"),
                order_data["payment_method"],
                order_id))
        return cursor.rowcount > 0

    # esta funcion es para eliminar una orden de la base de datos, 
    # se va a usar
    @staticmethod
    def delete(conn: sqlite3.Connection, order_id: int) -> bool:
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM orders 
            WHERE order_id = ? """, (order_id,))
        return cursor.rowcount > 0
    