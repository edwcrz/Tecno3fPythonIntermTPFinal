"""
Capa de servicio encargada de gestionar el ciclo de vida y la persistencia de la entidad Clientes 
mediante peticiones HTTP directas hacia el endpoint REST http://127.0.0.1:8000/customer.
"""
import requests
from typing import List, Dict, Optional, Tuple
from frontend.config import API_BASE_URL

class CustomerService:
    @staticmethod
    def get_all() -> Tuple[Optional[List[Dict]], Optional[str]]:
        try:
            res = requests.get(f"{API_BASE_URL}/customer/", timeout=5)
            if res.status_code == 200:
                return res.json(), None
            return None, res.json().get("detail", "Error cargando clientes")
        except requests.exceptions.RequestException as e:
            return None, f"Error de red: {e}"

    @staticmethod
    def create(name: str, email: str, phone: str) -> Tuple[Optional[Dict], Optional[str]]:
        try:
            res = requests.post(f"{API_BASE_URL}/customer/", json={"name": name, "email": email, "phone": phone}, timeout=5)
            if res.status_code == 201:
                return res.json(), None
            return None, res.json().get("detail", "Error creando cliente")
        except requests.exceptions.RequestException as e:
            return None, f"Error de red: {e}"

    @staticmethod
    def delete(customer_id: int) -> Tuple[bool, Optional[str]]:
        try:
            res = requests.delete(f"{API_BASE_URL}/customer/{customer_id}", timeout=5)
            if res.status_code == 200:
                return True, None
            return False, res.json().get("detail", "No se puede eliminar")
        except requests.exceptions.RequestException as e:
            return False, f"Error de red: {e}"