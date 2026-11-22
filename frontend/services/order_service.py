"""
/frontend/services/order_service.py
Pantalla PEDIDOS: agrupa orders + order_detail.
Las líneas usan el prefijo /order_detail. Los precios son una foto: los calcula el backend.
"""
from typing import Dict, List, Optional, Tuple

from frontend.services.api_client import request


class OrderService:

    # ---------- orders (cada pedido ya trae 'items', 'customer' y 'delivery_addresses') ----------
    @staticmethod
    def list_orders() -> Tuple[Optional[List[Dict]], Optional[str]]:
        return request("GET", "/order/", "No se pudo obtener la lista de pedidos")

    @staticmethod
    def get_order(order_id: int) -> Tuple[Optional[Dict], Optional[str]]:
        return request("GET", f"/order/{order_id}", "No se pudo obtener el pedido")

    @staticmethod
    def create_order(customer_id: int, payment_method_id: int, communication: Optional[str],
                     items: List[Dict]) -> Tuple[Optional[Dict], Optional[str]]:
        """items: [{"product_id": 1, "quantity": 3}, ...]"""
        payload = {"customer_id": customer_id, "payment_method_id": payment_method_id,
                   "communication": (communication or "").strip() or None, "items": items}
        return request("POST", "/order/", "No se pudo crear el pedido", json=payload)

    @staticmethod
    def change_state(order_id: int, state: str) -> Tuple[Optional[Dict], Optional[str]]:
        """state: 'confirmed' o 'cancelled'."""
        return request("PATCH", f"/order/{order_id}/state", "No se pudo cambiar el estado",
                       json={"state": state})

    # ---------- order_detail (solo mientras el pedido está pending) ----------
    @staticmethod
    def list_items(order_id: int) -> Tuple[Optional[List[Dict]], Optional[str]]:
        return request("GET", f"/order_detail/{order_id}/items", "No se pudieron obtener los ítems")

    @staticmethod
    def add_item(order_id: int, product_id: int, quantity: int) -> Tuple[Optional[List[Dict]], Optional[str]]:
        return request("POST", f"/order_detail/{order_id}/items", "No se pudo agregar el ítem",
                       json={"product_id": product_id, "quantity": quantity})

    @staticmethod
    def remove_item(order_id: int, order_detail_id: int) -> Tuple[Optional[List[Dict]], Optional[str]]:
        return request("DELETE", f"/order_detail/{order_id}/items/{order_detail_id}",
                       "No se pudo quitar el ítem")