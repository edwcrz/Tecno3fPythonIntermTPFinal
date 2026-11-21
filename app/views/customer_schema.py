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

class CustomerUpdate(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    customer_id: int
    class Config:
        from_attributes = True
