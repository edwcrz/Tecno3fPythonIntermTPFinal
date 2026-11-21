"""
/app/views/product_schema.py
"""

from pydantic import BaseModel, Field
from typing import Optional

"""
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    ingredients TEXT NULL,
    taste TEXT NULL,
    texture TEXT NULL,
    size TEXT NOT NULL,
    product_category TEXT NOT NULL,
    product_subcategory TEXT NULL,
    product_group TEXT NULL,
    product_subgroup TEXT NULL,
    stock INTEGER NOT NULL DEFAULT 0,
    reserved_stock INTEGER NOT NULL DEFAULT 0);
"""

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, example="Product Name")
    description: str = Field(..., min_length=1, max_length=100, example="Product Description")
    ingredients: Optional[str] = Field(None, max_length=100, example="Product Ingredients")
    taste: Optional[str] = Field(None, max_length=100, example="Product Taste")
    texture: Optional[str] = Field(None, max_length=100, example="Product Texture")
    size: str = Field(..., min_length=1, max_length=100, example="Product Size")
    product_category: str = Field(..., min_length=1, max_length=100, example="Product Category")
    product_subcategory: Optional[str] = Field(None, max_length=100, example="Product Subcategory")
    product_group: Optional[str] = Field(None, max_length=100, example="Product Group")
    product_subgroup: Optional[str] = Field(None, max_length=100, example="Product Subgroup")
    stock : int = Field(..., ge=0, example=10)
    reserved_stock : int = Field(..., ge=0, example=2)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductResponse(ProductBase):
    product_id: int
    class Config:
        from_attributes = True
