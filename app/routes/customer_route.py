from fastapi import APIRouter, Depends, status
import sqlite3
from typing import List
from app.database import get_db_connection

from app.controllers.customer_controller import CustomerController
from app.views.customer_schema import CustomerCreate, CustomerResponse, CustomerUpdate

router = APIRouter(prefix="/customer", tags=["Customer"])

@router.get("/", response_model=list[CustomerResponse])
def get_customers(db: sqlite3.Connection = Depends(get_db_connection)):
    return CustomerController.get_all(db)


@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db: sqlite3.Connection = Depends(get_db_connection)):
    return CustomerController.get(db, customer_id)


@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(body: CustomerCreate, db: sqlite3.Connection = Depends(get_db_connection)):
    return CustomerController.create(db, body.model_dump())


@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(customer_id: int, body: CustomerUpdate,
                    db: sqlite3.Connection = Depends(get_db_connection)):
    return CustomerController.update(db, customer_id, body.model_dump())


@router.delete("/{customer_id}", response_model=CustomerResponse)
def delete_customer(customer_id: int, db: sqlite3.Connection = Depends(get_db_connection)):
    return CustomerController.delete(db, customer_id)