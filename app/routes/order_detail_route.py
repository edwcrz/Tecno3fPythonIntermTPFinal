"""
/app/routes/order_detail_route.py
Líneas de un pedido: se agregan y se quitan mientras el pedido está pending.
"""
import sqlite3

from fastapi import APIRouter, Depends, status

from app.controllers.order_detail_controller import OrderDetailController
from app.database import get_db_connection
from app.views.order_schema import OrderDetailResponse, OrderItemCreate

router = APIRouter(prefix="/order_detail", tags=["Order Detail"])


@router.get("/{order_id}/items", response_model=list[OrderDetailResponse])
def get_items(order_id: int, db: sqlite3.Connection = Depends(get_db_connection)):
    return OrderDetailController.list_by_order(db, order_id)


@router.post("/{order_id}/items", response_model=list[OrderDetailResponse],
             status_code=status.HTTP_201_CREATED)
def add_item(order_id: int, item: OrderItemCreate,
             db: sqlite3.Connection = Depends(get_db_connection)):
    return OrderDetailController.add_item(db, order_id, item.product_id, item.quantity)


@router.delete("/{order_id}/items/{order_detail_id}", response_model=list[OrderDetailResponse])
def remove_item(order_id: int, order_detail_id: int,
                db: sqlite3.Connection = Depends(get_db_connection)):
    return OrderDetailController.remove_item(db, order_id, order_detail_id)