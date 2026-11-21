from pydantic import BaseModel, Field
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

class CustomerAddressBase(BaseModel):
    address: str = Field(..., min_length=1, max_length=200, example="Customer Address")
    locality: Optional[str] = Field(None, max_length=100, example="Customer Locality")
    province: Optional[str] = Field(None, max_length=100, example="Customer Province")
    pais: Optional[str] = Field(None, max_length=100, example="Customer Country")
    postal_code: Optional[str] = Field(None, max_length=20, example="Customer Postal Code")
    notes: Optional[str] = Field(None, max_length=200, example="Customer Notes")
    customer_id: int = Field(..., example=1)

class CustomerAddressCreate(CustomerAddressBase):
    pass

class CustomerAddressUpdate(CustomerAddressBase):
    pass

class CustomerAddressResponse(CustomerAddressBase):
    address_id: int

    class Config:
        from_attributes = True