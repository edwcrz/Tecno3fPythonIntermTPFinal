"""
/app/controllers/customer_controller.py
Reglas: email con formato válido y único, teléfono y edad coherentes, y
validate_can_buy() centraliza qué necesita un cliente para poder comprar.
"""
import sqlite3

from app.controllers.common_controller import (EMAIL_RE, PHONE_RE, conflict, invalid, not_found, non_negative_int, optional_text, required_text, transaction)
from app.models.customer_model import CustomerModel
from app.models.customer_address_model import CustomerAddressModel
from app.models.order_model import OrderModel


class CustomerController:

    @staticmethod
    def _row(db: sqlite3.Connection, customer_id: int) -> sqlite3.Row:
        row = CustomerModel.get_by_id(db, customer_id)
        if row is None:
            raise not_found("Cliente", customer_id)
        return row

    @staticmethod
    def _present(db: sqlite3.Connection, row: sqlite3.Row) -> dict:
        data = dict(row)
        data["addresses"] = [dict(a) for a in CustomerAddressModel.get_by_customer(db, row["customer_id"])]
        return data

    @staticmethod
    def _clean(db: sqlite3.Connection, data: dict, exclude_id: int | None = None) -> dict:
        email = optional_text(data.get("email"), "email", 120)
        if email:
            email = email.lower()
            if not EMAIL_RE.match(email):
                raise invalid("El email no tiene un formato válido")
            other = CustomerModel.get_by_email(db, email)
            if other is not None and other["customer_id"] != exclude_id:
                raise conflict("Ya existe un cliente con ese email")

        phone = optional_text(data.get("phone"), "phone", 20)
        if phone and not PHONE_RE.match(phone):
            raise invalid("El teléfono solo admite números, espacios, + - ( )")

        age = data.get("age")
        if age is not None:
            if isinstance(age, bool) or not isinstance(age, int) or not 0 <= age <= 120:
                raise invalid("'age' debe ser un número entre 0 y 120")
            age = str(age)  # la columna es TEXT

        return {
            "name": required_text(data.get("name"), "name"),
            "nickname": optional_text(data.get("nickname"), "nickname"),
            "surname": optional_text(data.get("surname"), "surname"),
            "email": email,
            "instagram": optional_text(data.get("instagram"), "instagram"),
            "phone": phone,
            "age": age,
            "gender": optional_text(data.get("gender"), "gender", 30),
            "likes": non_negative_int(data.get("likes") or 0, "likes"),
            "notes": optional_text(data.get("notes"), "notes", 500),
        }

    # ---------- consultas ----------
    @staticmethod
    def get_all(db: sqlite3.Connection) -> list[dict]:
        return [CustomerController._present(db, r) for r in CustomerModel.get_all(db)]

    @staticmethod
    def get(db: sqlite3.Connection, customer_id: int) -> dict:
        return CustomerController._present(db, CustomerController._row(db, customer_id))

    # ---------- regla de venta (la usa OrderController) ----------
    @staticmethod
    def validate_can_buy(db: sqlite3.Connection, customer_id: int) -> None:
        customer = CustomerModel.get_by_id(db, customer_id)
        if customer is None:
            raise not_found("Cliente", customer_id)
        if not (customer["email"] or "").strip():
            raise conflict("El cliente no tiene email registrado: no se puede vender")
        if CustomerAddressModel.count_by_customer(db, customer_id) == 0:
            raise conflict("El cliente no tiene dirección registrada: no se puede vender")

    # ---------- operaciones ----------
    @staticmethod
    def create(db: sqlite3.Connection, data: dict) -> dict:
        clean = CustomerController._clean(db, data)
        with transaction(db):
            new_id = CustomerModel.create(db, clean)
        return CustomerController.get(db, new_id)

    @staticmethod
    def update(db: sqlite3.Connection, customer_id: int, data: dict) -> dict:
        CustomerController._row(db, customer_id)
        clean = CustomerController._clean(db, data, exclude_id=customer_id)
        with transaction(db):
            CustomerModel.update(db, customer_id, clean)
        return CustomerController.get(db, customer_id)

    @staticmethod
    def delete(db: sqlite3.Connection, customer_id: int) -> dict:
        deleted = CustomerController.get(db, customer_id)
        if OrderModel.count_by_customer(db, customer_id) > 0:
            raise conflict("El cliente tiene pedidos: no se elimina para conservar el historial")
        with transaction(db):   # sin pedidos, sus direcciones se eliminan junto con él
            CustomerAddressModel.delete_by_customer(db, customer_id)
            CustomerModel.delete(db, customer_id)
        return deleted