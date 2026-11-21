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

class PaymentMethodUpdate(PaymentMethodBase):
    pass

class PaymentMethodResponse(PaymentMethodBase):
    payment_method_id: int
    class Config:
        from_attributes = True
