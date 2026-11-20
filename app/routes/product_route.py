from fastapi import APIRouter, Depends, status
import sqlite3
from typing import List
from database import get_db_connection

from app.models.product_model import ProductModel
from app.views import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter(prefix="/product", tags=["Product"])

@router.get("/", response_model=list[ProductResponse])
def get_product(db: sqlite3.Connection = Depends(get_db_connection)):
    return [dict(row) for row in ProductModel.get_all(db)]    

@router.get("/{product_id}", response_model=ProductResponse)
def get_product_by_id(product_id = int, db: sqlite3.Connection = Depends(get_db_connection)):
    return [ProductModel.get_by_id(db, product_id)]

@router.post("/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: sqlite3.Connection = Depends(get_db_connection)):
    return [ProductModel.create(db, product)]    

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductUpdate, db: sqlite3.Connection = Depends(get_db_connection)):
    return [ProductModel.update(db, product_id, product)]

@router.delete("/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
def delete_product(product_id = int, db: sqlite3.Connection = Depends(get_db_connection)):
    return [ProductModel.delete(db, product_id)]
