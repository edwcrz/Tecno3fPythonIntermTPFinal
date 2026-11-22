"""
/app/views/product_schema.py
Entrada: el cliente envía solo los datos del producto (y el stock inicial al crear).
reserved_stock y available los calcula el backend.
"""
from typing import Optional

from pydantic import BaseModel, Field

# Tabla (ver database.py):
#   product_id, name, description, ingredients, taste, texture, size,
#   product_category, product_subcategory, product_group, product_subgroup,
#   stock (físico), reserved_stock (comprometido en pedidos pending)


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, example="Crumble cookie")
    description: str = Field(..., min_length=1, max_length=300, example="Cookie con chips de chocolate")
    ingredients: Optional[str] = Field(None, max_length=100, example="Harina, manteca, chocolate")
    taste: Optional[str] = Field(None, max_length=100, example="Chocolate")
    texture: Optional[str] = Field(None, max_length=100, example="Crocante por fuera")
    size: str = Field(..., min_length=1, max_length=100, example="Individual")
    product_category: str = Field(..., min_length=1, max_length=100, example="Cookies")
    product_subcategory: Optional[str] = Field(None, max_length=100, example="Rellenas")
    product_group: Optional[str] = Field(None, max_length=100, example="Dulces")
    product_subgroup: Optional[str] = Field(None, max_length=100, example="Clásicos")


class ProductCreate(ProductBase):
    stock: int = Field(0, ge=0, example=10)   # stock inicial; reserved_stock arranca en 0


class ProductUpdate(ProductBase):
    pass   # el stock no se edita acá: se repone con /product/{id}/stock


class StockAdd(BaseModel):
    quantity: int = Field(..., gt=0, example=12)


class ProductResponse(ProductBase):
    product_id: int
    stock: int
    reserved_stock: int
    available: int   # stock - reserved_stock: lo que realmente se puede vender