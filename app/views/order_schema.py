from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

"""CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,

    customer_id INTEGER NOT NULL,
    date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    state TEXT NOT NULL DEFAULT 'pending',
    communication TEXT NULL,
    payment_method_id INTEGER NOT NULL,
    total DECIMAL(10,2) NOT NULL DEFAULT 0.01,
    
    FOREIGN KEY (customer_id) REFERENCES customer (customer_id) ON DELETE RESTRICT); """

class OrderBase(BaseModel):
    customer_id: int = Field(..., example=1)
    date: datetime = Field(..., example="2023-01-01 00:00:00")
    state: str = Field(..., min_length=1, max_length=100, example="pending")
    communication: Optional[str] = Field(None, max_length=200, example="pedido para Paracaidista Picasso")
    payment_methond: int = Field(..., gt=0)
    total: float = Field(..., gt=0, example=100.0)
        
class OrderCreate(OrderBase):
    pass

class OrderUpdate(OrderBase):
    pass

class OrderResponse(OrderBase):
    order_id: int
    class Config:
        from_attributes = True