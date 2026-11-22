"""
/app/views/order_schema.py
Lo que el cliente ENVÍA (OrderCreate, OrderItemCreate, OrderStateUpdate) es mínimo.
Fecha, estado inicial, precios y total los define el backend.
"""
from typing import Literal, Optional

from pydantic import BaseModel, Field


# ---------- entrada ----------
class OrderItemCreate(BaseModel):
    product_id: int = Field(..., gt=0, example=1)
    quantity: int = Field(..., gt=0, example=3)


class OrderCreate(BaseModel):
    customer_id: int = Field(..., gt=0, example=1)
    payment_method_id: int = Field(..., gt=0, example=1)
    communication: Optional[str] = Field(None, max_length=500, example="pedido para Paracaidista Picasso")
    items: list[OrderItemCreate] = Field(..., min_length=1)


class OrderStateUpdate(BaseModel):
    # 'pending' no es destino válido: un pedido nunca vuelve a pendiente
    state: Literal["confirmed", "cancelled"]


# ---------- salida ----------
class OrderDetailResponse(BaseModel):
    order_detail_id: int
    order_id: int
    product_id: int
    quantity: int
    unit_price: float   # foto del precio con recargo
    subtotal: float     # unit_price * quantity


class OrderCustomerResponse(BaseModel):
    customer_id: int
    name: str
    surname: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


class OrderResponse(BaseModel):
    order_id: int
    customer_id: int
    date: str
    state: str
    communication: Optional[str] = None
    payment_method_id: int
    total: float
    items: list[OrderDetailResponse] = Field(default_factory=list)
    customer: OrderCustomerResponse
    delivery_addresses: list[dict] = Field(default_factory=list)  # se leen del cliente