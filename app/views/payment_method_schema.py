"""
/app/views/payment_method_schema.py
overload es una fracción: 0.10 = 10% de recargo, 0.05 = 5%.
"""
from typing import Optional

from pydantic import BaseModel, Field

# Tabla (ver database.py):
#   payment_method_id INTEGER PRIMARY KEY AUTOINCREMENT,
#   method_name TEXT NOT NULL DEFAULT 'Efectivo',
#   overload (recargo, fracción), payment_term INTEGER,
#   payment_category TEXT NULL, payment_subcategory TEXT NULL


class PaymentMethodBase(BaseModel):
    method_name: str = Field(..., min_length=1, max_length=100, example="Tarjeta de crédito")
    overload: float = Field(0.0, ge=0.0, le=1.0, example=0.10)
    payment_term: int = Field(0, ge=0, example=0)
    payment_category: Optional[str] = Field(None, max_length=100, example="Tarjeta")
    payment_subcategory: Optional[str] = Field(None, max_length=100, example="Crédito")


class PaymentMethodCreate(PaymentMethodBase):
    pass


class PaymentMethodUpdate(PaymentMethodBase):
    pass


class PaymentMethodResponse(PaymentMethodBase):
    payment_method_id: int
