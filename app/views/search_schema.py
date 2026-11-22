"""
/app/views/search_schema.py
Respuestas de los buscadores.
"""
from typing import Optional

from pydantic import BaseModel

from app.views.customer_schema import CustomerResponse
from app.views.product_schema import ProductResponse


class CustomerSearchResponse(CustomerResponse):
    can_buy: bool
    reason: str          # "Puede comprar", "Falta email", "Falta dirección"


class ProductSearchItem(ProductResponse):
    base_price: Optional[float] = None
    sellable: bool       # tiene precio base y stock disponible


class ProductSearchResponse(BaseModel):
    query: str
    total: int
    results: list[ProductSearchItem]