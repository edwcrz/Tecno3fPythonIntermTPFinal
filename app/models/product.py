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
    stock INTEGER NOT NULL DEFAULT 0);
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

class ProductModel:

    # esta funcion es para obtener todos los productos de la base de datos, se va a usar en el endpoint GET /product
    @staticmethod
    def get_all(conn: sqlite3.Connection) -> list[sqlite3.Row]:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT product_id, name, description, ingredients, taste, texture, size, product_category, product_subcategory, product_group, product_subgroup, stock 
            FROM product""")
        return cursor.fetchall()

    # esta funcion es para obtener un producto por su id de la base de datos, se va a usar en el endpoint GET /product/{product_id}
    @staticmethod
    def get_by_id(conn: sqlite3.Connection, product_id: int) -> Optional[sqlite3.Row]:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT product_id, name, description, ingredients, taste, texture, size, product_category, product_subcategory, product_group, product_subgroup, stock 
            FROM product 
            WHERE product_id = ?""", (product_id,))
        return cursor.fetchone()

    # esta funcion es para crear un producto en la base de datos, se va a usar en el endpoint POST /product
    # va a recibir un diccionario con los datos del producto, y va a devolver el id del producto creado, 
    # para eso vamos a usar el metodo lastrowid del cursor, que devuelve el id del ultimo registro insertado
    @staticmethod   
    def create(conn: sqlite3.Connection, product_data: dict) -> int:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO product (name, description, ingredients, taste, texture, size, product_category, product_subcategory, product_group, product_subgroup, stock)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
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
                product_data["stock",0]))
        conn.commit()
        return cursor.lastrowid

    # esta funcion es para actualizar un producto en la base de datos, se va a usar en el endpoint PUT /product/{product_id}
    @staticmethod
    def update(conn: sqlite3.Connection, product_id: int, product_data: dict) -> bool:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE product
            SET name = ?, description = ?, ingredients = ?, taste = ?, texture = ?, size = ?, product_category = ?, product_subcategory = ?, product_group = ?, product_subgroup = ?, stock = ?
            WHERE product_id = ?""", (
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
                product_data["stock",0],
                product_id))
        conn.commit()
        return cursor.rowcount > 0

    # esta funcion es para eliminar un producto de la base de datos, se va a usar en el endpoint DELETE /product/{product_id}
    @staticmethod
    def delete(conn: sqlite3.Connection, product_id: int) -> bool:
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM product 
            WHERE product_id = ?""", (product_id,))
        conn.commit()
        return cursor.rowcount > 0
    