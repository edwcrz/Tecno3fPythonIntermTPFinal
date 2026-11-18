from pydantic import BaseModel, Field
from typing import Optional

"""
CREATE TABLE IF NOT EXISTS payment_method (
    payment_method_id INTEGER PRIMARY KEY AUTOINCREMENT,
    method_name TEXT NOT NULL DEFAULT "Efectivo",
    overload decimal(2, 2) NOT NULL DEFAULT 0.00,
    payment_term INTEGER NOT NULL DEFAULT 0,
    payment_category TEXT NULL);
    payment_subcategory TEXT NULL);
"""
        
class PaymentMethodBase(BaseModel):
    method_name: str = Field(..., min_length=1, max_length=100, example="Efectivo")
    overload: float = Field(..., ge=0.00, example=0.00)
    payment_term: int = Field(..., ge=0, example=0)
    payment_category: Optional[str] = Field(None, max_length=100,example="Categoria 1")
    payment_subcategory: Optional[str] = Field(None, max_length=100, example="Subcategoria 1")
    
class PaymentMethodCreate(PaymentMethodBase):   
    pass
    # va a heredar todos los campos de PaymentMethodBase, es para crear un método de pago, no necesita el payment_method_id porque se va a generar automaticamente
    # se usa en la validación del cuerpo de los post, cuando creamos un método de pago vamos a validar que venga con este formato de datos
    # el pass no agrega nada adicional para que continue de manera normal, es solo para que no de error de sintaxis, porque no tiene ningun metodo ni atributo adicional

class PaymentMethodUpdate(PaymentMethodBase):
    pass
    # va a heredar todos los campos de PaymentMethodBase, es para actualizar un método de pago, no necesita el payment_method_id porque se va a generar automaticamente
    # se usa en la validación del cuerpo de los put, cuando actualizamos un método de pago vamos a validar que venga con este formato de datos
    # el pass no agrega nada adicional para que continue de manera normal, es solo para que no de error de sintaxis, porque no tiene ningun metodo ni atributo adicional

class PaymentMethodResponse(PaymentMethodBase):
    payment_method_id: int
    # no hace falta validar con el field porque es un campo que se va a generar automaticamente, no es un campo que venga del cliente, es un campo que viene de la base de datos
    # viene de la base de datos, es el id del método de pago, es un campo que se va a generar automaticamente, no es un campo que venga del cliente, es un campo que viene de la base de datos
    class Config:
        from_attributes = True
        # sirve para que pydantic pueda trabajar con objetos de tipo ORM, y no de diccionarios, si no se pone esto, pydantic no va a poder trabajar con objetos de tipo ORM, y va a dar error al intentar convertir un objeto de tipo ORM a un objeto de tipo Pydantic
        # si no se pone esta linea, pydantic no va a poder trabajar con objetos de tipo ORM, y va a dar error al intentar convertir un objeto de tipo ORM a un objeto de tipo Pydantic
