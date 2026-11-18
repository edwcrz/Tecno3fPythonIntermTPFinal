from pydantic import BaseModel, Field
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

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, example="Product Name")
    description: str = Field(..., min_length=1, max_length=100, example="Product Description")
    ingredients: Optional[str] = Field(None, max_length=100, example="Product Ingredients")
    taste: Optional[str] = Field(None, max_length=100, example="Product Taste")
    texture: Optional[str] = Field(None, max_length=100, example="Product Texture")
    size: str = Field(..., min_length=1, max_length=100, example="Product Size")
    product_category: str = Field(..., min_length=1, max_length=100, example="Product Category")
    product_subcategory: Optional[str] = Field(None, max_length=100, example="Product Subcategory")
    product_group: Optional[str] = Field(None, max_length=100, example="Product Group")
    product_subgroup: Optional[str] = Field(None, max_length=100, example="Product Subgroup")
    stock : int = Field(..., ge=0, example=10)

class ProductCreate(ProductBase):
    pass
    # va a heredar todos los campos de ProductBase, es para crear un producto, no necesita el product_id porque se va a generar automaticamente
    # se usa en la validación del cuerpo de los post, cuando creamos un producto vamos a validar que venga con este formato de datos
    # el pass no agrega nada adicional para que continue de manera normal, es solo para que no de error de sintaxis, porque no tiene ningun metodo ni atributo adicional

class ProductUpdate(ProductBase):
    pass
    # va a heredar todos los campos de ProductBase, es para actualizar un producto, no necesita el product_id porque se va a generar automaticamente
    # se usa en la validación del cuerpo de los put, cuando actualizamos un producto vamos a validar que venga con este formato de datos
    # el pass no agrega nada adicional para que continue de manera normal, es solo para que no de error de sintaxis, porque no tiene ningun metodo ni atributo adicional

class ProductResponse(ProductBase):
    product_id: int
    # no hace falta validar con el field porque es un campo que se va a generar automaticamente, no es un campo que venga del cliente, es un campo que viene de la base de datos
    # viene de la base de datos, es el id del producto, es un campo que se va a generar automaticamente, no es un campo que venga del cliente, es un campo que viene de la base de datos
    class Config:
        from_attributes = True
        # sirve para que pydantic pueda trabajar con objetos de tipo ORM, y no de diccionarios, si no se pone esto, pydantic no va a poder trabajar con objetos de tipo ORM, y va a dar error al intentar convertir un objeto de tipo ORM a un objeto de tipo Pydantic
        # si no se pone esta linea, pydantic no va a poder trabajar con objetos de tipo ORM, y va a dar error al intentar convertir un objeto de tipo ORM a un objeto de tipo Pydantic
