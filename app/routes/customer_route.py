from fastapi import APIRouter, Depends, status
import sqlite3
from typing import List
from app.database import get_db_connection

from app.models.customer_model import CustomerModel
from app.views.customer_schema import CustomerCreate, CustomerResponse, CustomerUpdate

router = APIRouter(prefix="/customer", tags=["Customer"])

@router.get("/", response_model=list[CustomerResponse])
def get_customer(db: sqlite3.Connection = Depends(get_db_connection)):
    return [dict(row) for row in CustomerModel.get_all(db)]    

@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer_by_id(customer_id = int, db: sqlite3.Connection = Depends(get_db_connection)):
    return [CustomerModel.get_by_id(db, customer_id)]

@router.post("/", response_model=CustomerResponse)
def create_customer(customer: CustomerCreate, db: sqlite3.Connection = Depends(get_db_connection)):
    return [CustomerModel.create(db, customer)]    

@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(customer_id: int, customer: CustomerUpdate, db: sqlite3.Connection = Depends(get_db_connection)):
    return [CustomerModel.update(db, customer_id, customer)]

@router.delete("/{customer_id}", response_model=CustomerResponse, status_code=status.HTTP_200_OK)
def delete_customer(customer_id = int, db: sqlite3.Connection = Depends(get_db_connection)):
    return [CustomerModel.delete(db, customer_id)]





