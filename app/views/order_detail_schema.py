from pydantic import BaseModel, Field
from typing import Optional

"""
    CREATE TABLE IF NOT EXISTS order_detail (
        order_detail_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        unit_price REAL NOT NULL,
    )"""

class OrderDetailBase(BaseModel):
    order_id: int = Field(..., example=1)
    product_id: int = Field(..., example=1)
    quantity: int = Field(..., ge=1, example=1)
    unit_price: float = Field(..., ge=0, example=10.0)
        
class OrderDetailCreate(OrderDetailBase):
    pass
    # va a heredar todos los campos de OrderDetailBase, es para crear un detalle de orden, no necesita el order_detail_id porque se va a generar automaticamente
    # se usa en la validación del cuerpo de los post, cuando creamos un detalle de orden vamos a validar que venga con este formato de datos
    # el pass no agrega nada adicional para que continue de manera normal, es solo para que no de error de sintaxis, porque no tiene ningun metodo ni atributo adicional

class OrderDetailUpdate(OrderDetailBase):
    pass
    # va a heredar todos los campos de OrderDetailBase, es para actualizar un detalle de orden, no necesita el order_detail_id porque se va a generar automaticamente
    # se usa en la validación del cuerpo de los put, cuando actualizamos un detalle de orden vamos a validar que venga con este formato de datos
    # el pass no agrega nada adicional para que continue de manera normal, es solo para que no de error de sintaxis, porque no tiene ningun metodo ni atributo adicional

class OrderDetailResponse(OrderDetailBase):
    order_detail_id: int
    # no hace falta validar con el field porque es un campo que se va a generar automaticamente, no es un campo que venga del cliente, es un campo que viene de la base de datos
    # viene de la base de datos, es el id del producto, es un campo que se va a generar automaticamente, no es un campo que venga del cliente, es un campo que viene de la base de datos
    class Config:
        from_attributes = True
        # sirve para que pydantic pueda trabajar con objetos de tipo ORM, y no de diccionarios, si no se pone esto, pydantic no va a poder trabajar con objetos de tipo ORM, y va a dar error al intentar convertir un objeto de tipo ORM a un objeto de tipo Pydantic
        # si no se pone esta linea, pydantic no va a poder trabajar con objetos de tipo ORM, y va a dar error al intentar convertir un objeto de tipo ORM a un objeto de tipo Pydantic
