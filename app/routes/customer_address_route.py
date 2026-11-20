from fastapi import APIRouter, Depends, status
import sqlite3
from typing import List
from database import get_db_connection

from app.models.customer_address_model import CustomerAddressModel
from app.views import CustomerAddressCreate, CustomerAddressResponse, CustomerAddressUpdate

router = APIRouter(prefix="/customer_address", tags=["CustomerAddress"])

@router.get("/", response_model=list[CustomerAddressResponse])
def get_customer_address(db: sqlite3.Connection = Depends(get_db_connection)):
    return [dict(row) for row in CustomerAddressModel.get_all(db)]    

@router.get("/{customer_address_id}", response_model=CustomerAddressResponse)
def get_customer_address_by_id(customer_address_id = int, db: sqlite3.Connection = Depends(get_db_connection)):
    return [CustomerAddressModel.get_by_id(db, customer_address_id)]

@router.post("/", response_model=CustomerAddressResponse)
def create_customer_address(customer_address: CustomerAddressCreate, db: sqlite3.Connection = Depends(get_db_connection)):
    return [CustomerAddressModel.create(db, customer_address)]    

@router.put("/{customer_address_id}", response_model=CustomerAddressResponse)
def update_customer_address(customer_address_id: int, customer_address: CustomerAddressUpdate, db: sqlite3.Connection = Depends(get_db_connection)):
    return [CustomerAddressModel.update(db, customer_address_id, customer_address)]

@router.delete("/{customer_address_id}", response_model=CustomerAddressResponse, status_code=status.HTTP_200_OK)
def delete_customer_address(customer_address_id = int, db: sqlite3.Connection = Depends(get_db_connection)):
    return [CustomerAddressModel.delete(db, customer_address_id)]