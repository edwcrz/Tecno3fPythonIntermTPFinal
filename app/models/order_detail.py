import sqlite3
from typing import Optional

"""
    CREATE TABLE IF NOT EXISTS order_detail (
        order_detail_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        unit_price REAL NOT NULL,
    )"""

# class OrderDetailBase(BaseModel):
#    order_id: int = Field(..., example=1)
#    product_id: int = Field(..., example=1)
#    quantity: int = Field(..., ge=1, example=1)
#    unit_price: float = Field(..., ge=0, example=10.0)
        
class OrderDetailModel:

    @staticmethod
    # esta funcion es para obtener todos los detalles de orden de la base de datos, se va a usar en el endpoint GET /order_details
    def get_all(conn: sqlite3.Connection) -> list[sqlite3.Row]:
        cursor = conn.cursor()
        cursor.execute("SELECT order_detail_id, order_id, product_id, quantity, unit_price FROM order_detail")
        return cursor.fetchall()

    @staticmethod
    # esta funcion es para obtener un detalle de orden por su id de la base de datos, se va a usar en el endpoint GET /order_details/{order_detail_id}
    def get_by_id(conn: sqlite3.Connection, order_detail_id: int) -> Optional[sqlite3.Row]:
        cursor = conn.cursor()
        cursor.execute("SELECT order_detail_id, order_id, product_id, quantity, unit_price FROM order_detail WHERE order_detail_id = ?", (order_detail_id,))
        return cursor.fetchone()

    @staticmethod
    def create(conn: sqlite3.Connection, order_detail_data: dict) -> int:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO order_detail (order_id, product_id. quantity, unit_price)
            VALUES (?, ?, ?, ?, ?)
        """, (
            order_detail_data["order_id"],
            order_detail_data["product_id"],
            order_detail_data["quantity"],
            order_detail_data["unit_price"],
        ))
        return cursor.lastrowid             

    @staticmethod
    # esta funcion es para actualizar una orden en la base de datos, se va a usar
    # va a recibir el id de la orden a actualizar y un diccionario con los nuevos datos
    def update(conn: sqlite3.Connection, order_detail_id: int, order_detail_data: dict) -> bool:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE order_detail
            SET order_id = ?, product_id = ?, quantity = ?, unit_price = ?
            WHERE order_id = ?
        """, (
            order_detail_data["order_id"],
            order_detail_data["product_id"],
            order_detail_data["quantity"],
            order_detail_data["unit_price"],
            order_detail_id
        ))
        return cursor.rowcount > 0  
            
## borrado físico en la base de datos, no es recomendable, porque se pierde la información, 
## es mejor hacer un borrado lógico, cambiando el estado del cliente a inactivo
## solo borrar una orden que no tenga ordenes asociadas, para eso vamos a hacer una consulta a la tabla orders,

    @staticmethod
    # esta funcion es para eliminar una orden de la base de datos, se va a usar
    def delete(conn: sqlite3.Connection, order_detail_id: int) -> bool:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM order_detail WHERE order_detail_id = ?", (order_detail_id,))
        return cursor.rowcount > 0
    