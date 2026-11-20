from fastapi import APIRouter, Depends, status
import sqlite3
from typing import List
from database import get_db_connection

from app.models.payment_method_model import PaymentMethodModel
from app.views import PaymentMethodCreate, PaymentMethodResponse, PaymentMethodUpdate

router = APIRouter(prefix="/payment_method", tags=["PaymentMethod"])

@router.get("/", response_model=list[PaymentMethodResponse])
def get_product_payment(db: sqlite3.Connection = Depends(get_db_connection)):
    return [dict(row) for row in PaymentMethodModel.get_all(db)]    

@router.get("/{payment_method_id}", response_model=PaymentMethodResponse)
def get_payment_method_by_id(payment_method_id = int, db: sqlite3.Connection = Depends(get_db_connection)):
    return [PaymentMethodModel.get_by_id(db, payment_method_id)]

@router.post("/", response_model=PaymentMethodResponse)
def create_payment_method(payment_method: PaymentMethodCreate, db: sqlite3.Connection = Depends(get_db_connection)):
    return [PaymentMethodModel.create(db, payment_method)]    

@router.put("/{payment_method_id}", response_model=PaymentMethodResponse)
def update_payment_method(payment_method_id: int, payment_method: PaymentMethodUpdate, db: sqlite3.Connection = Depends(get_db_connection)):
    return [PaymentMethodModel.update(db, payment_method_id, payment_method)]

@router.delete("/{payment_method_id}", response_model=PaymentMethodResponse, status_code=status.HTTP_200_OK)
def delete_payment_method(payment_method_id = int, db: sqlite3.Connection = Depends(get_db_connection)):
    return [PaymentMethodModel.delete(db, payment_method_id)]