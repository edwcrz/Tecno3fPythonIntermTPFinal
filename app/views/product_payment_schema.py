"""
/app/views/product_payment_schema.py
Un solo precio base por producto, cargado con un método de recargo 0.
Los precios finales por método se calculan: base * (1 + overload).
"""
from pydantic import BaseModel, Field

# Tabla (ver database.py):
#   product_payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
#   product_id INTEGER NOT NULL, payment_method_id INTEGER NOT NULL,
#   price DECIMAL(10,2) NOT NULL DEFAULT 0.01, currency TEXT DEFAULT 'Pesos'


class ProductPaymentCreate(BaseModel):
    product_id: int = Field(..., ge=1, example=1)
    payment_method_id: int = Field(..., ge=1, example=1)   # debe ser un método sin recargo
    price: float = Field(..., ge=0.01, example=10000.0)
    currency: str = Field("Pesos", min_length=1, max_length=30, example="Pesos")


class ProductPaymentUpdate(BaseModel):
    payment_method_id: int = Field(..., ge=1, example=1)
    price: float = Field(..., ge=0.01, example=10000.0)
    currency: str = Field("Pesos", min_length=1, max_length=30, example="Pesos")


class ProductPaymentResponse(BaseModel):
    product_payment_id: int
    product_id: int
    payment_method_id: int
    price: float
    currency: str


# ---------- precios finales (solo lectura) ----------
class FinalPrice(BaseModel):
    payment_method_id: int
    method_name: str
    overload: float
    final_price: float


class PriceListResponse(BaseModel):
    product_id: int
    name: str
    base_price: float
    currency: str
    prices: list[FinalPrice]