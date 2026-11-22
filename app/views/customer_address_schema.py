"""
/app/views/customer_address_schema.py
La dirección pertenece a un cliente y no se mueve de cliente: customer_id solo se envía al crear.
"""

from pydantic import BaseModel, Field
from typing import Optional

"""
    CREATE TABLE IF NOT EXISTS customer_address (
        address_id INTEGER PRIMARY KEY AUTOINCREMENT,
        address TEXT NOT NULL,
        locality TEXT NULL,
        province TEXT NULL,
        country TEXT NULL,
        postal_code TEXT NULL,
        notes TEXT NULL,
        customer_id INTEGER NOT NULL,
"""

# Tabla (ver database.py):
#   address_id INTEGER PRIMARY KEY AUTOINCREMENT,
#   address TEXT NOT NULL, locality TEXT NULL, province TEXT NULL,
#   country TEXT NULL, postal_code TEXT NULL, notes TEXT NULL,
#   customer_id INTEGER NOT NULL (FK a customer)


class CustomerAddressBase(BaseModel):
    address: str = Field(..., min_length=1, max_length=200, example="Av. Rivadavia 1234, 3ºB")
    locality: Optional[str] = Field(None, max_length=100, example="Caseros")
    province: Optional[str] = Field(None, max_length=100, example="Buenos Aires")
    country: Optional[str] = Field(None, max_length=100, example="Argentina")
    postal_code: Optional[str] = Field(None, max_length=20, example="B1678")
    notes: Optional[str] = Field(None, max_length=500, example="Tocar timbre 3B")


class CustomerAddressCreate(CustomerAddressBase):
    customer_id: int = Field(..., gt=0, example=1)


class CustomerAddressUpdate(CustomerAddressBase):
    pass


class CustomerAddressResponse(CustomerAddressBase):
    address_id: int
    customer_id: int