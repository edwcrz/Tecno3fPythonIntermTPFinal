"""
Capa intermedia de abstracción para Productos. 
Proporciona una interfaz unificada mediante métodos estáticos que desacoplan las vistas de los detalles HTTP de ProductApiService.
en http://127.0.0.1:5000/product
"""
import requests
from typing import List, Dict, Optional, Tuple
from frontend.config import API_BASE_URL

class ProductService:
    @staticmethod
    def get_all() -> Tuple[Optional[List[Dict]], Optional[str]]:
        try:
            res = requests.get(f"{API_BASE_URL}/product/", timeout=5)
            if res.status_code == 200:
                return res.json(), None
            return None, f"Error {res.status_code}: No se pudo obtener la lista"
        except requests.exceptions.RequestException as e:
            return None, f"Sin conexión con el servidor: {e}"

    @staticmethod
    def create(name: str, price: float, stock: int) -> Tuple[Optional[Dict], Optional[str]]:
        payload = {"name": name, "price": price, "stock": stock}
        try:
            res = requests.post(f"{API_BASE_URL}/product/", json=payload, timeout=5)
            if res.status_code == 201:
                return res.json(), None
            return None, f"Error {res.status_code}: No se pudo crear el producto"
        except requests.exceptions.RequestException as e:
            return None, f"Error de red: {e}"

    @staticmethod
    def update(product_id: int, name: str, price: float, stock: int) -> Tuple[Optional[Dict], Optional[str]]:
        payload = {"name": name, "price": price, "stock": stock}
        try:
            res = requests.put(f"{API_BASE_URL}/product/{product_id}", json=payload, timeout=5)
            if res.status_code == 200:
                return res.json(), None
            return None, f"Error {res.status_code}: No se pudo actualizar"
        except requests.exceptions.RequestException as e:
            return None, f"Error de red: {e}"

    @staticmethod
    def delete(product_id: int) -> Tuple[bool, Optional[str]]:
        try:
            res = requests.delete(f"{API_BASE_URL}/product/{product_id}", timeout=5)
            if res.status_code == 200:
                return True, None
            return False, f"Error {res.status_code}: No se pudo eliminar"
        except requests.exceptions.RequestException as e:
            return False, f"Error de red: {e}"