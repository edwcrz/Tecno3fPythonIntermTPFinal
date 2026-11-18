import sqlite3
from typing import Optional
from datetime import datetime

"""CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    state TEXT NOT NULL DEFAULT 'pending',
    communication TEXT NULL,
    payment_method NOT NULL DEFAULT 'efectivo',
    )"""

# class OrderBase(BaseModel):
#  customer_id: int = Field(..., example=1)
#  date: datetime = Field(..., example="2023-01-01 00:00:00")
#  quantity: int = Field(..., ge=0, example=1)
#  state: str = Field(..., min_length=1, max_length=100, example="pending")
#  communication: Optional[str] = Field(None, max_length=200, example="Order Communication")
#  payment_methond: str = Field(..., min_length=1, max_length=100, example="efectivo")

class OrdersModel:

    @staticmethod
    # esta funcion es para obtener todas las ordenes de la base de datos, se va a usar en el endpoint GET /orders
    def get_all(conn: sqlite3.Connection) -> list[sqlite3.Row]:
        cursor = conn.cursor()
        cursor.execute("SELECT customer_id, date, quantity, state, communication, payment_method FROM orders")
        return cursor.fetchall()

    @staticmethod
    # esta funcion es para obtener una orden por su id de la base de datos, se va a usar en el endpoint GET /orders/{order_id}
    def get_by_id(conn: sqlite3.Connection, order_id: int) -> Optional[sqlite3.Row]:
        cursor = conn.cursor()
        cursor.execute("SELECT customer_id, date, quantity, state, communication, payment_method FROM orders WHERE order_id = ?", (order_id,))
        return cursor.fetchone()        

    @staticmethod
    # esta funcion es para crear una orden en la base de datos, se va a usar en el endpoint POST /orders
    # va a recibir un diccionario con los datos de la orden, y va a devolver el id de la orden creada
    # para eso vamos a usar el metodo lastrowid del cursor, que devuelve el id del ultimo registro insertado
    def create(conn: sqlite3.Connection, order_data: dict) -> int:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO orders (customer_id, date, quantity, state, communication, payment_method)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            order_data["customer_id"],
            order_data["date"],
            order_data["quantity"],
            order_data["state"],
            order_data.get("communication"),
            order_data["payment_methond"]
        ))
        return cursor.lastrowid             

    @staticmethod
    # esta funcion es para actualizar una orden en la base de datos, se va a usar
    # va a recibir el id de la orden a actualizar y un diccionario con los nuevos datos
    def update(conn: sqlite3.Connection, order_id: int, order_data: dict) -> bool:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE orders
            SET customer_id = ?, date = ?, quantity = ?, state = ?, communication = ?, payment_method = ?
            WHERE order_id = ?
        """, (
            order_data["customer_id"],
            order_data["date"],
            order_data["quantity"],
            order_data["state"],
            order_data.get("communication"),
            order_data["payment_method"],
            order_id
        ))
        return cursor.rowcount > 0  
            
## borrado físico en la base de datos, no es recomendable, porque se pierde la información, 
## es mejor hacer un borrado lógico, cambiando el estado del cliente a inactivo
## solo borrar una orden que no tenga ordenes asociadas, para eso vamos a hacer una consulta a la tabla orders,

    @staticmethod
    # esta funcion es para eliminar una orden de la base de datos, se va a usar
    def delete(conn: sqlite3.Connection, order_id: int) -> bool:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM orders WHERE order_id = ?", (order_id,))
        return cursor.rowcount > 0
    