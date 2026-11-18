from pydantic import BaseModel, Field
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

class CustomerBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, example="Customer Name")
    nickname: Optional[str] = Field(None, max_length=100, example="Customer Nickname")
    surname: Optional[str] = Field(None, max_length=100, example="Customer Surname")
    email: Optional[str] = Field(None, max_length=100, example="Customer Email")
    instagram: Optional[str] = Field(None, max_length=100, example="Customer Instagram")
    phone: Optional[str] = Field(None, max_length=12, example="Customer Phone")
    age: Optional[int] = Field(None, le=150, example="Customer Age")
    gender: Optional[str] = Field(None, max_length=100, example="Customer Gender")
    likes: int = Field(None, ge=0, example=0)   
    notes: Optional[str] = Field(None, max_length=200, example="Customer Notes  ")
    
class CustomerCreate(CustomerBase):
    pass
    # va a heredar todos los campos de CustomerBase, es para crear un cliente, no necesita el customer_id porque se va a generar automaticamente
    # se usa en la validación del cuerpo de los post, cuando creamos un cliente vamos a validar que venga con este formato de datos
    # el pass no agrega nada adicional para que continue de manera normal, es solo para que no de error de sintaxis, porque no tiene ningun metodo ni atributo adicional

class CustomerUpdate(CustomerBase):
    pass
    # va a heredar todos los campos de CustomerBase, es para actualizar un cliente, no necesita el customer_id porque se va a generar automaticamente
    # se usa en la validación del cuerpo de los put, cuando actualizamos un cliente vamos a validar que venga con este formato de datos
    # el pass no agrega nada adicional para que continue de manera normal, es solo para que no de error de sintaxis, porque no tiene ningun metodo ni atributo adicional

class CustomerResponse(CustomerBase):
    customer_id: int
    # no hace falta validar con el field porque es un campo que se va a generar automaticamente, no es un campo que venga del cliente, es un campo que viene de la base de datos
    # viene de la base de datos, es el id del producto, es un campo que se va a generar automaticamente, no es un campo que venga del cliente, es un campo que viene de la base de datos
    class Config:
        from_attributes = True
        # sirve para que pydantic pueda trabajar con objetos de tipo ORM, y no de diccionarios, si no se pone esto, pydantic no va a poder trabajar con objetos de tipo ORM, y va a dar error al intentar convertir un objeto de tipo ORM a un objeto de tipo Pydantic
        # si no se pone esta linea, pydantic no va a poder trabajar con objetos de tipo ORM, y va a dar error al intentar convertir un objeto de tipo ORM a un objeto de tipo Pydantic
