from pydantic import BaseModel, Field
from typing import Optional

"""
CREATE TABLE IF NOT EXISTS order_detail (
    order_detail_id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price REAL NOT NULL CHECK (unit_price >= 0),
    subtotal DECIMAL(10,2) NOT NULL DEFAULT 0.01,

    FOREIGN KEY (order_id) REFERENCES orders (order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES product (product_id) ON DELETE RESTRICT); """

class OrderDetailBase(BaseModel):
    order_id: int = Field(..., example=1)
    product_id: int = Field(..., example=1)
    quantity: int = Field(..., gt=0, example=1)
    unit_price: float = Field(..., gt=0, example=10.0)
    subtotal: float = Field(..., gt=0, example=100.0)
        
class OrderDetailCreate(OrderDetailBase):
    pass

class OrderDetailUpdate(OrderDetailBase):
    pass

class OrderDetailResponse(OrderDetailBase):
    order_detail_id: int
    class Config:
        from_attributes = True