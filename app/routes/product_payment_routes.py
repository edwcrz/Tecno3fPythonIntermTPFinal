from fastapi import APIRouter, Depends, status
import sqlite3
from typing import List
from database import get_db_connection

from app.models.product_payment_model import ProductPaymentModel
from app.views import ProductPaymentCreate, ProductPaymentResponse, ProductPaymentUpdate

router = APIRouter(prefix="/product_payment", tags=["ProductPayment"])

@router.get("/", response_model=list[ProductPaymentResponse])
def get_product_payment(db: sqlite3.Connection = Depends(get_db_connection)):
    return [dict(row) for row in ProductPaymentModel.get_all(db)]    

@router.get("/{product_payment_id}", response_model=ProductPaymentResponse)
def get_product_payment_by_id(product_payment_id = int, db: sqlite3.Connection = Depends(get_db_connection)):
    return [ProductPaymentModel.get_by_id(db, product_payment_id)]

@router.post("/", response_model=ProductPaymentResponse)
def create_product_payment(product_payment: ProductPaymentCreate, db: sqlite3.Connection = Depends(get_db_connection)):
    return [ProductPaymentModel.create(db, product_payment)]    

@router.put("/{product_payment_id}", response_model=ProductPaymentResponse)
def update_product_payment(product_payment_id: int, product_payment: ProductPaymentUpdate, db: sqlite3.Connection = Depends(get_db_connection)):
    return [ProductPaymentModel.update(db, product_payment_id, product_payment)]

@router.delete("/{product_payment_id}", response_model=ProductPaymentResponse, status_code=status.HTTP_200_OK)
def delete_product_payment(product_payment_id = int, db: sqlite3.Connection = Depends(get_db_connection)):
    return [ProductPaymentModel.delete(db, product_payment_id)]