from pydantic import BaseModel, Field
from typing import Optional

"""
CREATE TABLE IF NOT EXISTS product_payment (
    product_payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    payment_method_id INTEGER NOT NULL,
    price DECIMAL(10, 2) NOT NULL DEFAULT 0.01,
    currency TEXT NULL DEFAULT "Pesos",
"""
        
class ProductPaymentBase(BaseModel):
    product_id: int = Field(..., ge=1, example=1)
    payment_method_id: int = Field(..., ge=1, example=1)
    price: float = Field(..., ge=0.01, example=10.99)
    currency: str = Field(..., min_length=1, max_length=100, example="Pesos")
    
class ProductPaymentCreate(ProductPaymentBase):
    pass
    # va a heredar todos los campos de ProductPaymentBase, es para crear un pago de producto, no necesita el product_payment_id porque se va a generar automaticamente
    # se usa en la validación del cuerpo de los post, cuando creamos un pago de producto vamos a validar que venga con este formato de datos
    # el pass no agrega nada adicional para que continue de manera normal, es solo para que no de error de sintaxis, porque no tiene ningun metodo ni atributo adicional

class ProductPaymentUpdate(ProductPaymentBase):
    pass
    # va a heredar todos los campos de ProductPaymentBase, es para actualizar un pago de producto, no necesita el product_payment_id porque se va a generar automaticamente
    # se usa en la validación del cuerpo de los put, cuando actualizamos un pago de producto vamos a validar que venga con este formato de datos
    # el pass no agrega nada adicional para que continue de manera normal, es solo para que no de error de sintaxis, porque no tiene ningun metodo ni atributo adicional

class ProductPaymentResponse(ProductPaymentBase):
    product_payment_id: int
    # no hace falta validar con el field porque es un campo que se va a generar automaticamente, no es un campo que venga del cliente, es un campo que viene de la base de datos
    # viene de la base de datos, es el id del producto, es un campo que se va a generar automaticamente, no es un campo que venga del cliente, es un campo que viene de la base de datos
    class Config:
        from_attributes = True
        # sirve para que pydantic pueda trabajar con objetos de tipo ORM, y no de diccionarios, si no se pone esto, pydantic no va a poder trabajar con objetos de tipo ORM, y va a dar error al intentar convertir un objeto de tipo ORM a un objeto de tipo Pydantic
        # si no se pone esta linea, pydantic no va a poder trabajar con objetos de tipo ORM, y va a dar error al intentar convertir un objeto de tipo ORM a un objeto de tipo Pydantic
