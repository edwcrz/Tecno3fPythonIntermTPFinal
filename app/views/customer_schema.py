"""
/app/views/customer_schema.py
"""
from typing import Optional
from pydantic import BaseModel, Field

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

"""
/app/views/customer_schema.py
"""
class CustomerBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, example="Ana")
    nickname: Optional[str] = Field(None, max_length=100, example="Anita")
    surname: Optional[str] = Field(None, max_length=100, example="Pérez")
    email: Optional[str] = Field(None, max_length=120, example="ana@mail.com")
    instagram: Optional[str] = Field(None, max_length=100, example="@ana.dulces")
    phone: Optional[str] = Field(None, max_length=20, example="+54 11 1234-5678")
    age: Optional[int] = Field(None, ge=0, le=120, example=30)
    gender: Optional[str] = Field(None, max_length=30, example="Femenino")
    likes: int = Field(0, ge=0, example=0)
    notes: Optional[str] = Field(None, max_length=500, example="Prefiere sin frutos secos")

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    customer_id: int
    addresses: list[dict] = Field(default_factory=list)  # lo agrega CustomerController._present