"""
/app/routes/product_route.py
Rutas finitas: reciben, delegan en ProductController y responden.
"""
import sqlite3

from fastapi import APIRouter, Depends, status

from app.controllers.product_controller import ProductController
from app.database import get_db_connection
from app.views.product_schema import ProductCreate, ProductResponse, ProductUpdate, StockAdd

router = APIRouter(prefix="/product", tags=["Product"])


@router.get("/", response_model=list[ProductResponse])
def get_products(db: sqlite3.Connection = Depends(get_db_connection)):
    return ProductController.get_all(db)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: sqlite3.Connection = Depends(get_db_connection)):
    return ProductController.get(db, product_id)


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: sqlite3.Connection = Depends(get_db_connection)):
    return ProductController.create(db, product.model_dump())


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductUpdate,
                   db: sqlite3.Connection = Depends(get_db_connection)):
    return ProductController.update(db, product_id, product.model_dump())


@router.post("/{product_id}/stock", response_model=ProductResponse)
def add_stock(product_id: int, body: StockAdd, db: sqlite3.Connection = Depends(get_db_connection)):
    return ProductController.add_stock(db, product_id, body.quantity)


@router.delete("/{product_id}", response_model=ProductResponse)
def delete_product(product_id: int, db: sqlite3.Connection = Depends(get_db_connection)):
    return ProductController.delete(db, product_id)