from fastapi import APIRouter, Depends, status
import sqlite3
from typing import List
from app.database import get_db_connection

from app.models.order_model import OrderModel
from app.views import OrderCreate, OrderResponse, OrderUpdate

router = APIRouter(prefix="/order", tags=["Order"])

@router.get("/", response_model=list[OrderResponse])
def get_orders(db: sqlite3.Connection = Depends(get_db_connection)):
    return [dict(row) for row in OrderModel.get_all(db)]    

@router.get("/{order_id}", response_model=OrderResponse)
def get_order_by_id(order_id = int, db: sqlite3.Connection = Depends(get_db_connection)):
    return [OrderModel.get_by_id(db, order_id)]

@router.post("/", response_model=OrderResponse)
def create_order(order: OrderCreate, db: sqlite3.Connection = Depends(get_db_connection)):
    return [OrderModel.create(db, order)]    

@router.put("/{order_id}", response_model=OrderResponse)
def update_order(order_id: int, order: OrderUpdate, db: sqlite3.Connection = Depends(get_db_connection)):
    return [OrderModel.update(db, order_id, order)]

@router.delete("/{order_id}", response_model=OrderResponse, status_code=status.HTTP_200_OK)
def delete_order(order_id = int, db: sqlite3.Connection = Depends(get_db_connection)):
    return [OrderModel.delete(db, order_id)]