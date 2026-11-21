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

class ProductPaymentUpdate(ProductPaymentBase):
    pass

class ProductPaymentResponse(ProductPaymentBase):
    product_payment_id: int
    class Config:
        from_attributes = True