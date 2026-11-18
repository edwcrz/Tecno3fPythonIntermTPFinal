from pydantic import BaseModel, Field
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

class OrderBase(BaseModel):
    customer_id: int = Field(..., example=1)
    date: datetime = Field(..., example="2023-01-01 00:00:00")
    quantity: int = Field(..., ge=0, example=1)
    state: str = Field(..., min_length=1, max_length=100, example="pending")
    communication: Optional[str] = Field(None, max_length=200, example="Order Communication")
    payment_methond: str = Field(..., min_length=1, max_length=100, example="efectivo")
        
class OrderCreate(OrderBase):
    pass
    # va a heredar todos los campos de OrderBase, es para crear un orden, no necesita el order_id porque se va a generar automaticamente
    # se usa en la validación del cuerpo de los post, cuando creamos un orden vamos a validar que venga con este formato de datos
    # el pass no agrega nada adicional para que continue de manera normal, es solo para que no de error de sintaxis, porque no tiene ningun metodo ni atributo adicional

class OrderUpdate(OrderBase):
    pass
    # va a heredar todos los campos de OrderBase, es para actualizar un orden, no necesita el order_id porque se va a generar automaticamente
    # se usa en la validación del cuerpo de los put, cuando actualizamos un orden vamos a validar que venga con este formato de datos
    # el pass no agrega nada adicional para que continue de manera normal, es solo para que no de error de sintaxis, porque no tiene ningun metodo ni atributo adicional

class OrderResponse(OrderBase):
    order_id: int
    # no hace falta validar con el field porque es un campo que se va a generar automaticamente, no es un campo que venga del cliente, es un campo que viene de la base de datos
    # viene de la base de datos, es el id del producto, es un campo que se va a generar automaticamente, no es un campo que venga del cliente, es un campo que viene de la base de datos
    class Config:
        from_attributes = True
        # sirve para que pydantic pueda trabajar con objetos de tipo ORM, y no de diccionarios, si no se pone esto, pydantic no va a poder trabajar con objetos de tipo ORM, y va a dar error al intentar convertir un objeto de tipo ORM a un objeto de tipo Pydantic
        # si no se pone esta linea, pydantic no va a poder trabajar con objetos de tipo ORM, y va a dar error al intentar convertir un objeto de tipo ORM a un objeto de tipo Pydantic
