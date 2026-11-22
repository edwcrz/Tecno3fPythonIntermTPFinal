"""
/app/routes/order_route.py
Rutas finitas: reciben, delegan en OrderController y responden.
"""
import sqlite3

from fastapi import APIRouter, Depends, status

from app.controllers.order_controller import OrderController
from app.database import get_db_connection
from app.views.order_schema import OrderCreate, OrderResponse, OrderStateUpdate

router = APIRouter(prefix="/order", tags=["Order"])


@router.get("/", response_model=list[OrderResponse])
def get_orders(db: sqlite3.Connection = Depends(get_db_connection)):
    return OrderController.get_all(db)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: sqlite3.Connection = Depends(get_db_connection)):
    return OrderController.get(db, order_id)


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate, db: sqlite3.Connection = Depends(get_db_connection)):
    return OrderController.create(
        db,
        order.customer_id,
        order.payment_method_id,
        order.communication,
        [item.model_dump() for item in order.items],
    )


@router.patch("/{order_id}/state", response_model=OrderResponse)
def change_order_state(order_id: int, body: OrderStateUpdate,
                       db: sqlite3.Connection = Depends(get_db_connection)):
    return OrderController.change_state(db, order_id, body.state)