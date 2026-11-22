"""
/app/routes/customer_address_route.py
"""
import sqlite3

from fastapi import APIRouter, Depends, status

from app.controllers.customer_address_controller import CustomerAddressController
from app.database import get_db_connection
from app.views.customer_address_schema import (CustomerAddressCreate, CustomerAddressResponse, CustomerAddressUpdate)

router = APIRouter(prefix="/customer_address", tags=["Customer Address"])


# Va antes de "/{address_id}" para que "customer" no se confunda con un id
@router.get("/customer/{customer_id}", response_model=list[CustomerAddressResponse])
def get_addresses_by_customer(customer_id: int, db: sqlite3.Connection = Depends(get_db_connection)):
    return CustomerAddressController.list_by_customer(db, customer_id)


@router.get("/{address_id}", response_model=CustomerAddressResponse)
def get_address(address_id: int, db: sqlite3.Connection = Depends(get_db_connection)):
    return CustomerAddressController.get(db, address_id)


@router.post("/", response_model=CustomerAddressResponse, status_code=status.HTTP_201_CREATED)
def create_address(body: CustomerAddressCreate, db: sqlite3.Connection = Depends(get_db_connection)):
    return CustomerAddressController.create(db, body.model_dump())


@router.put("/{address_id}", response_model=CustomerAddressResponse)
def update_address(address_id: int, body: CustomerAddressUpdate,
                   db: sqlite3.Connection = Depends(get_db_connection)):
    return CustomerAddressController.update(db, address_id, body.model_dump())


@router.delete("/{address_id}", response_model=CustomerAddressResponse)
def delete_address(address_id: int, db: sqlite3.Connection = Depends(get_db_connection)):
    return CustomerAddressController.delete(db, address_id)