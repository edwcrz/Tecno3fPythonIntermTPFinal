"""
Servicio encargado de la comunicación HTTP directa con el backend REST de Productos. 
Encapsula las solicitudes GET, POST, PUT y DELETE capturando excepciones de red para evitar caídas en la interfaz.
Toma los clicks y los traduce a las funciones de la API, habla con el Backend
"""
import requests
from typing import List, Dict, Optional, Tuple
from frontend.config import API_BASE_URL

class ProductApiService:
    @staticmethod
    def get_all_products() -> Tuple[Optional[List[Dict]], Optional[str]]:
        try:
            res = requests.get(f"{API_BASE_URL}/product/", timeout=5)
            if res.status_code == 200:
                return res.json(), None
            return None, f"Error {res.status_code}: No se pudo obtener la lista"
        except requests.exceptions.RequestException as e:
            return None, f"Fallo de conexión con la API: {e}"

    @staticmethod
    def create_product(data: Dict) -> Tuple[Optional[Dict], Optional[str]]:
        try:
            res = requests.post(f"{API_BASE_URL}/product/", json=data, timeout=5)
            if res.status_code == 201:
                return res.json(), None
            return None, f"Error {res.status_code}: No se pudo crear el producto"
        except requests.exceptions.RequestException as e:
            return None, f"Fallo de conexión: {e}"

    @staticmethod
    def update_product(product_id: int, data: Dict) -> Tuple[Optional[Dict], Optional[str]]:
        try:
            res = requests.put(f"{API_BASE_URL}/product/{product_id}", json=data, timeout=5)
            if res.status_code == 200:
                return res.json(), None
            return None, f"Error {res.status_code}: No se pudo actualizar el producto"
        except requests.exceptions.RequestException as e:
            return None, f"Fallo de conexión: {e}"

    @staticmethod
    def delete_product(product_id: int) -> Tuple[bool, Optional[str]]:
        try:
            res = requests.delete(f"{API_BASE_URL}/product/{product_id}", timeout=5)
            if res.status_code == 200:
                return True, None
            return False, f"Error {res.status_code}: No se pudo eliminar el producto"
        except requests.exceptions.RequestException as e:
            return False, f"Fallo de conexión: {e}"