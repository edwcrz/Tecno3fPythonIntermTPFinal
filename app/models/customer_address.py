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

class CustomerAddressModel:

    # esta funcion es para obtener todos los detalles de customer adddress de la base de datos, 
    # se va a usar en el endpoint GET /customer_address
    @staticmethod
    def get_all(conn: sqlite3.Connection) -> list[sqlite3.Row]:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT address_id, address, locality, province, pais, postal_code, notes, customer_id 
            FROM customer_address""")
        return cursor.fetchall()
    
    # esta funcion es para obtener un detalle de customer address por su id de la base de datos, 
    # se va a usar en el endpoint GET /customer_address/{address_id}
    @staticmethod
    def get_by_id(conn: sqlite3.Connection, address_id: str) -> Optional[sqlite3.Row]:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT address_id, address, locality, province, pais, postal_code, notes, customer_id 
            FROM customer_address 
            WHERE address_id = ?""", (address_id,))
        return cursor.fetchone()

    # esta funcion es para obtener un detalle de customer address por su customer id de la base de datos, 
    # se va a usar en el endpoint GET /customer_address/{customer_id}
    @staticmethod
    def get_by_id(conn: sqlite3.Connection, customer_id: str) -> Optional[sqlite3.Row]:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT address_id, address, locality, province, pais, postal_code, notes, customer_id 
            FROM customer_address 
            WHERE customer_id = ?""", (customer_id,))
        return cursor.fetchone()

    # esta funcion es para crear una customer_address en la base de datos, 
    # se va a usar
    # va a recibir un diccionario con los nuevos datos
    @staticmethod
    def create(conn: sqlite3.Connection, customer_address_data: dict) -> int:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO customer_address (address, locality, province, pais, postal_code, notes, customer_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)""", (
                customer_address_data["address"],
                customer_address_data["locality"],
                customer_address_data["province"],
                customer_address_data["pais"],
                customer_address_data["postal_code"],
                customer_address_data["notes"],
                customer_address_data["customer_id"]))
        return cursor.lastrowid             

    # esta funcion es para actualizar una customer_address en la base de datos, 
    # se va a usar
    # va a recibir el address_id a actualizar y un diccionario con los nuevos datos    
    @staticmethod
    def update(conn: sqlite3.Connection, address_id: int, customer_address_data: dict) -> bool:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE customer_address
            SET address = ?, locality = ?, province = ?, pais = ?, postal_code = ?, notes = ?, customer_id = ?
            WHERE address = ? """, (
                customer_address_data["address"],
                customer_address_data["locality"],
                customer_address_data["province"],
                customer_address_data["pais"],
                customer_address_data["postal_code"],
                customer_address_data["notes"],
                customer_address_data["customer_id"],
                address_id))
        return cursor.rowcount > 0  
               
    # esta funcion es para borrar una customer_address en la base de datos, 
    # se va a usar
    # va a recibir el address_id a borrar
    @staticmethod
    # esta funcion es para eliminar una orden de la base de datos, se va a usar
    def delete(conn: sqlite3.Connection, address_id: str) -> bool:
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM customer_address 
            WHERE address = ?""", (address_id,))
        return cursor.rowcount > 0
