from fastapi import APIRouter, Depends, status
import sqlite3
from typing import List
from database import get_db_connection

from app.models.order_detail_models import OrderDetailModel
from app.views import OrderDetailCreate, OrderDetailResponse, OrderDetailUpdate

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.get("/", response_model=list[OrderDetailResponse])
def get_order_detail(db: sqlite3.Connection = Depends(get_db_connection)):
    return [dict(row) for row in OrderDetailModel.get_all(db)]    

@router.get("/{order_detail_id}", response_model=OrderDetailResponse)
def get_order_detail_by_id(order_detail_id = int, db: sqlite3.Connection = Depends(get_db_connection)):
    return [OrderDetailModel.get_by_id(db, order_detail_id)]

@router.post("/", response_model=OrderDetailResponse)
def create_order_detail(order_detail: OrderDetailCreate, db: sqlite3.Connection = Depends(get_db_connection)):
    return [OrderDetailModel.create(db, order_detail)]    

@router.put("/{order_detail_id}", response_model=OrderDetailResponse)
def update_order_detail(order_detail_id: int, order_detail: OrderDetailUpdate, db: sqlite3.Connection = Depends(get_db_connection)):
    return [OrderDetailModel.update(db, order_detail_id, order_detail)]

@router.delete("/{order_detail_id}", response_model=OrderDetailResponse, status_code=status.HTTP_200_OK)
def delete_order_detail(order_detail_id = int, db: sqlite3.Connection = Depends(get_db_connection)):
    return [OrderDetailModel.delete(db, order_detail_id)]