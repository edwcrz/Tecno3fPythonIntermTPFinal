"""
/app/controllers/customer_address_controller.py
Reglas: la dirección pertenece a un cliente existente y no se mueve de cliente.
No se borra la única dirección de un cliente con pedidos pendientes (delivery).
"""
import sqlite3

from app.controllers.common_controller import conflict, not_found, optional_text, required_text, transaction
from app.models.customer_model import CustomerModel
from app.models.customer_address_model import CustomerAddressModel
from app.models.order_model import OrderModel


class CustomerAddressController:

    @staticmethod
    def _row(db: sqlite3.Connection, address_id: int) -> sqlite3.Row:
        row = CustomerAddressModel.get_by_id(db, address_id)
        if row is None:
            raise not_found("Dirección", address_id)
        return row

    @staticmethod
    def _clean(data: dict) -> dict:
        return {
            "address": required_text(data.get("address"), "address", 200),
            "locality": optional_text(data.get("locality"), "locality"),
            "province": optional_text(data.get("province"), "province"),
            "pais": optional_text(data.get("pais"), "pais"),
            "postal_code": optional_text(data.get("postal_code"), "postal_code", 20),
            "notes": optional_text(data.get("notes"), "notes", 500),
        }

    @staticmethod
    def list_by_customer(db: sqlite3.Connection, customer_id: int) -> list[dict]:
        if CustomerModel.get_by_id(db, customer_id) is None:
            raise not_found("Cliente", customer_id)
        return [dict(r) for r in CustomerAddressModel.get_by_customer(db, customer_id)]

    @staticmethod
    def get(db: sqlite3.Connection, address_id: int) -> dict:
        return dict(CustomerAddressController._row(db, address_id))

    @staticmethod
    def create(db: sqlite3.Connection, data: dict) -> dict:
        customer_id = data.get("customer_id")
        if CustomerModel.get_by_id(db, customer_id) is None:
            raise not_found("Cliente", customer_id)
        clean = CustomerAddressController._clean(data)
        clean["customer_id"] = customer_id
        with transaction(db):
            new_id = CustomerAddressModel.create(db, clean)
        return CustomerAddressController.get(db, new_id)

    @staticmethod
    def update(db: sqlite3.Connection, address_id: int, data: dict) -> dict:
        current = CustomerAddressController._row(db, address_id)
        clean = CustomerAddressController._clean(data)
        clean["customer_id"] = current["customer_id"]   # ignora cualquier intento de cambiarlo
        with transaction(db):
            CustomerAddressModel.update(db, address_id, clean)
        return CustomerAddressController.get(db, address_id)

    @staticmethod
    def delete(db: sqlite3.Connection, address_id: int) -> dict:
        current = CustomerAddressController._row(db, address_id)
        customer_id = current["customer_id"]
        if (CustomerAddressModel.count_by_customer(db, customer_id) == 1
                and OrderModel.count_pending_by_customer(db, customer_id) > 0):
            raise conflict("Es la única dirección del cliente y tiene pedidos pendientes")
        deleted = dict(current)
        with transaction(db):
            CustomerAddressModel.delete(db, address_id)
        return deleted