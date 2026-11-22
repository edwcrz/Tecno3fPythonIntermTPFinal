"""
/app/routes/product_payment_route.py
"""
import sqlite3

from fastapi import APIRouter, Depends, status

from app.controllers.product_payment_controller import ProductPaymentController
from app.database import get_db_connection
from app.views.product_payment_schema import (PriceListResponse, ProductPaymentCreate,
                                              ProductPaymentResponse, ProductPaymentUpdate)

router = APIRouter(prefix="/product_payment", tags=["Product Payment"])


@router.get("/", response_model=list[ProductPaymentResponse])
def get_product_payments(db: sqlite3.Connection = Depends(get_db_connection)):
    return ProductPaymentController.get_all(db)


# Va antes de "/{product_payment_id}" para que "product" no se confunda con un id
@router.get("/product/{product_id}/prices", response_model=PriceListResponse)
def get_price_list(product_id: int, db: sqlite3.Connection = Depends(get_db_connection)):
    return ProductPaymentController.price_list(db, product_id)


@router.get("/{product_payment_id}", response_model=ProductPaymentResponse)
def get_product_payment(product_payment_id: int, db: sqlite3.Connection = Depends(get_db_connection)):
    return ProductPaymentController.get(db, product_payment_id)


@router.post("/", response_model=ProductPaymentResponse, status_code=status.HTTP_201_CREATED)
def create_product_payment(body: ProductPaymentCreate, db: sqlite3.Connection = Depends(get_db_connection)):
    return ProductPaymentController.create(db, body.model_dump())


@router.put("/{product_payment_id}", response_model=ProductPaymentResponse)
def update_product_payment(product_payment_id: int, body: ProductPaymentUpdate,
                           db: sqlite3.Connection = Depends(get_db_connection)):
    return ProductPaymentController.update(db, product_payment_id, body.model_dump())


@router.delete("/{product_payment_id}", response_model=ProductPaymentResponse)
def delete_product_payment(product_payment_id: int, db: sqlite3.Connection = Depends(get_db_connection)):
    return ProductPaymentController.delete(db, product_payment_id)