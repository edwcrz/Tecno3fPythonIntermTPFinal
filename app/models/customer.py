import sqlite3
from typing import Optional

"""
CREATE TABLE IF NOT EXISTS customer (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    nickname TEXT NULL,
    surname TEXT NULL,
    email TEXT NULL,
    instagram TEXT NULL,
    phone TEXT NULL,
    age TEXT NULL,
    gender TEXT NULL,
    likes INTEGER NULL DEFAULT 0,
    notes TEXT NULL);   
"""

#class CustomerBase(BaseModel):
#  name: str = Field(..., min_length=1, max_length=100, example="Customer Name")
#  nickname: Optional[str] = Field(None, max_length=100, example="Customer Nickname")
#  surname: Optional[str] = Field(None, max_length=100, example="Customer Surname")
#  email: Optional[str] = Field(None, max_length=100, example="Customer Email")
#  instagram: Optional[str] = Field(None, max_length=100, example="Customer Instagram")
#  phone: Optional[str] = Field(None, max_length=12, example="Customer Phone")
#  age: Optional[int] = Field(None, le=150, example="Customer Age")
#  gender: Optional[str] = Field(None, max_length=100, example="Customer Gender")
#  likes: int = Field(None, ge=0, example=0)   
#  notes: Optional[str] = Field(None, max_length=200, example="Customer Notes  ")

class CustomerModel:

    # esta funcion es para obtener todos los clientes de la base de datos, se va a usar en el endpoint GET /customer
    @staticmethod
    def get_all(conn: sqlite3.Connection) -> list[sqlite3.Row]:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT customer_id, name, nickname, surname, email, instagram, phone, age, gender, likes, notes 
            FROM customer""")
        return cursor.fetchall()

    # esta funcion es para obtener un cliente por su id de la base de datos
    @staticmethod
    def get_by_id(conn: sqlite3.Connection, customer_id: int) -> Optional[sqlite3.Row]:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT customer_id, name, nickname, surname, email, instagram, phone, age, gender, likes, notes 
            FROM customer 
            WHERE customer_id = ?""", (customer_id,))
        return cursor.fetchone()

    # esta funcion es para crear un cliente en la base de datos, se va a usar en el endpoint POST /customer
    # va a recibir un diccionario con los datos del cliente, y va a devolver el id del cliente creado, 
    # para eso vamos a usar el metodo lastrowid del cursor, que devuelve el id del ultimo registro insertado
    @staticmethod
    def create(conn: sqlite3.Connection, customer_data: dict) -> int:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO customer (name, nickname, surname, email, instagram, phone, age, gender, likes, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
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

    # esta funcion es para actualizar un cliente en la base de datos, se va a usar
    # va a recibir el id del cliente a actualizar y un diccionario con los nuevos datos
    @staticmethod
    def update(conn: sqlite3.Connection, customer_id: int, customer_data: dict) -> bool:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE customer
            SET name = ?, nickname = ?, surname = ?, email = ?, instagram = ?, phone = ?, age = ?, gender = ?, likes = ?, notes = ?
            WHERE customer_id = ?""", (
                customer_data["name"],
                customer_data("nickname"),
                customer_data("surname"),
                customer_data("email"),
                customer_data("instagram"),
                customer_data("phone"),
                customer_data("age"),
                customer_data("gender"),
                customer_data("likes", 0),
                customer_data("notes"),
                customer_id))
        return cursor.rowcount > 0

    # esta funcion es para eliminar un cliente de la base de datos, se va a usar
    @staticmethod
    def delete(conn: sqlite3.Connection, customer_id: int) -> bool:
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM customer 
            WHERE customer_id = ?""", (customer_id,))
        return cursor.rowcount > 0 