"""
/frontend/services/customer_service.py
Pantalla CLIENTES: agrupa customer + customer_address.
Para vender, el cliente necesita email y al menos una dirección.
"""
from typing import Dict, List, Optional, Tuple

from frontend.services.api_client import clean, request

CUSTOMER_FIELDS = ("name", "nickname", "surname", "email", "instagram", "phone",
                   "age", "gender", "likes", "notes")
ADDRESS_FIELDS = ("address", "locality", "province", "country", "postal_code", "notes")


def _customer_payload(data: Dict) -> Dict:
    payload = clean(data, CUSTOMER_FIELDS)
    age = payload.get("age")
    payload["age"] = int(age) if str(age or "").isdigit() else None   # el backend espera un número
    payload["likes"] = int(payload.get("likes") or 0)
    return payload


class CustomerService:

    # ---------- customer (cada cliente ya trae su lista 'addresses') ----------
    @staticmethod
    def list_customers() -> Tuple[Optional[List[Dict]], Optional[str]]:
        return request("GET", "/customer/", "No se pudo obtener la lista de clientes")

    @staticmethod
    def create_customer(data: Dict) -> Tuple[Optional[Dict], Optional[str]]:
        return request("POST", "/customer/", "No se pudo crear el cliente", json=_customer_payload(data))

    @staticmethod
    def update_customer(customer_id: int, data: Dict) -> Tuple[Optional[Dict], Optional[str]]:
        return request("PUT", f"/customer/{customer_id}", "No se pudo actualizar el cliente",
                       json=_customer_payload(data))

    @staticmethod
    def delete_customer(customer_id: int) -> Tuple[bool, Optional[str]]:
        _, err = request("DELETE", f"/customer/{customer_id}", "No se pudo eliminar el cliente")
        return err is None, err

    # ---------- customer_address ----------
    @staticmethod
    def list_addresses(customer_id: int) -> Tuple[Optional[List[Dict]], Optional[str]]:
        return request("GET", f"/customer_address/customer/{customer_id}",
                       "No se pudieron obtener las direcciones")

    @staticmethod
    def create_address(customer_id: int, data: Dict) -> Tuple[Optional[Dict], Optional[str]]:
        payload = clean(data, ADDRESS_FIELDS)
        payload["customer_id"] = customer_id     # solo se envía al crear
        return request("POST", "/customer_address/", "No se pudo crear la dirección", json=payload)

    @staticmethod
    def update_address(address_id: int, data: Dict) -> Tuple[Optional[Dict], Optional[str]]:
        return request("PUT", f"/customer_address/{address_id}", "No se pudo actualizar la dirección",
                       json=clean(data, ADDRESS_FIELDS))

    @staticmethod
    def delete_address(address_id: int) -> Tuple[bool, Optional[str]]:
        _, err = request("DELETE", f"/customer_address/{address_id}", "No se pudo eliminar la dirección")
        return err is None, err

    # ---------- ayuda para la vista ----------
    @staticmethod
    def sale_status(customer: Dict) -> Tuple[bool, str]:
        """Dice si el cliente puede comprar y, si no, por qué (misma regla que el backend)."""
        if not (customer.get("email") or "").strip():
            return False, "Falta email"
        if not customer.get("addresses"):
            return False, "Falta dirección"
        return True, "Puede comprar"