"""
/app/routes/payment_method_route.py
"""
import sqlite3

from fastapi import APIRouter, Depends, status

from app.controllers.payment_method_controller import PaymentMethodController
from app.database import get_db_connection
from app.views.payment_method_schema import (PaymentMethodCreate, PaymentMethodResponse, PaymentMethodUpdate)

router = APIRouter(prefix="/payment_method", tags=["Payment Method"])


@router.get("/", response_model=list[PaymentMethodResponse])
def get_payment_methods(db: sqlite3.Connection = Depends(get_db_connection)):
    return PaymentMethodController.get_all(db)


@router.get("/{method_id}", response_model=PaymentMethodResponse)
def get_payment_method(method_id: int, db: sqlite3.Connection = Depends(get_db_connection)):
    return PaymentMethodController.get(db, method_id)


@router.post("/", response_model=PaymentMethodResponse, status_code=status.HTTP_201_CREATED)
def create_payment_method(body: PaymentMethodCreate, db: sqlite3.Connection = Depends(get_db_connection)):
    return PaymentMethodController.create(db, body.model_dump())


@router.put("/{method_id}", response_model=PaymentMethodResponse)
def update_payment_method(method_id: int, body: PaymentMethodUpdate,
                          db: sqlite3.Connection = Depends(get_db_connection)):
    return PaymentMethodController.update(db, method_id, body.model_dump())


@router.delete("/{method_id}", response_model=PaymentMethodResponse)
def delete_payment_method(method_id: int, db: sqlite3.Connection = Depends(get_db_connection)):
    return PaymentMethodController.delete(db, method_id)