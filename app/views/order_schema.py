"""
/app/views/order_schema.py
Lo que el cliente ENVÍA (OrderCreate, OrderItemCreate, OrderStateUpdate) es mínimo.
Fecha, estado inicial, precios y total los define el backend.
"""
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
    date: Optional[datetime] = Field[None, example="2023-01-01 00:00:00"]
    state: Optional[str] = Field[None, min_length=1, max_length=100, example="pending"]
    communication: Optional[str] = Field(None, max_length=200, example="pedido para Paracaidista Picasso")
    payment_method: int = Field(..., gt=0)
    total: Optional[float] = Field[None, gt=0, example=100.0]
        
"""
/app/views/order_schema.py
Lo que el cliente ENVÍA (OrderCreate, OrderItemCreate, OrderStateUpdate) es mínimo.
Fecha, estado inicial, precios y total los define el backend.
"""
from typing import Literal, Optional

from pydantic import BaseModel, Field

# Tablas (ver database.py):
#   orders: order_id, customer_id, date, state (pending|confirmed|cancelled),
#           communication, payment_method_id, total
#   order_detail: order_detail_id, order_id, product_id, quantity, unit_price, subtotal


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