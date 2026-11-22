"""
/frontend/services/search_service.py
Buscadores contra la URL central /search del backend:
- Cliente por email (búsqueda exacta, resultado único)
- Producto por texto (%texto%)
- Producto por ingrediente (%texto% sobre el campo ingredients)
"""
from typing import Dict, Optional, Tuple

from frontend.services.api_client import request


class SearchService:
    @staticmethod
    def customer_by_email(email: str) -> Tuple[Optional[Dict], Optional[str]]:
        return request("GET", "/search/customer", "No se pudo buscar el cliente",
                       params={"email": email.strip()})

    @staticmethod
    def products(text: str) -> Tuple[Optional[Dict], Optional[str]]:
        return request("GET", "/search/product", "No se pudo buscar el producto",
                       params={"q": text.strip()})

    @staticmethod
    def ingredient(text: str) -> Tuple[Optional[Dict], Optional[str]]:
        return request("GET", "/search/ingredient", "No se pudo buscar por ingrediente",
                       params={"q": text.strip()})