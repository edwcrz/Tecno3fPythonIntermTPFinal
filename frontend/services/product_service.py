"""
/frontend/services/product_service.py
Pantalla PRODUCTOS: agrupa product + payment_method + product_payment.
overload es una fracción (0.10 = 10%). El precio base se carga con un método sin recargo.
"""
from typing import Dict, List, Optional, Tuple

from frontend.services.api_client import clean, request

PRODUCT_FIELDS = ("name", "description", "size", "product_category", "ingredients", "taste",
                  "texture", "product_subcategory", "product_group", "product_subgroup")
METHOD_FIELDS = ("method_name", "overload", "payment_term", "payment_category", "payment_subcategory")


class ProductService:

    # ---------- product ----------
    @staticmethod
    def list_products() -> Tuple[Optional[List[Dict]], Optional[str]]:
        return request("GET", "/product/", "No se pudo obtener la lista de productos")

    @staticmethod
    def create_product(data: Dict, stock: int = 0) -> Tuple[Optional[Dict], Optional[str]]:
        payload = clean(data, PRODUCT_FIELDS)
        payload["stock"] = stock          # stock inicial: solo al crear
        return request("POST", "/product/", "No se pudo crear el producto", json=payload)

    @staticmethod
    def update_product(product_id: int, data: Dict) -> Tuple[Optional[Dict], Optional[str]]:
        # sin stock: se repone con add_stock
        return request("PUT", f"/product/{product_id}", "No se pudo actualizar el producto",
                       json=clean(data, PRODUCT_FIELDS))

    @staticmethod
    def add_stock(product_id: int, quantity: int) -> Tuple[Optional[Dict], Optional[str]]:
        return request("POST", f"/product/{product_id}/stock", "No se pudo reponer el stock",
                       json={"quantity": quantity})

    @staticmethod
    def delete_product(product_id: int) -> Tuple[bool, Optional[str]]:
        _, err = request("DELETE", f"/product/{product_id}", "No se pudo eliminar el producto")
        return err is None, err

    # ---------- payment_method ----------
    @staticmethod
    def list_methods() -> Tuple[Optional[List[Dict]], Optional[str]]:
        return request("GET", "/payment_method/", "No se pudieron obtener los métodos de pago")

    @staticmethod
    def create_method(data: Dict) -> Tuple[Optional[Dict], Optional[str]]:
        return request("POST", "/payment_method/", "No se pudo crear el método de pago",
                       json=clean(data, METHOD_FIELDS))

    @staticmethod
    def update_method(method_id: int, data: Dict) -> Tuple[Optional[Dict], Optional[str]]:
        return request("PUT", f"/payment_method/{method_id}", "No se pudo actualizar el método de pago",
                       json=clean(data, METHOD_FIELDS))

    @staticmethod
    def delete_method(method_id: int) -> Tuple[bool, Optional[str]]:
        _, err = request("DELETE", f"/payment_method/{method_id}", "No se pudo eliminar el método de pago")
        return err is None, err

    # ---------- product_payment (precio base) ----------
    @staticmethod
    def list_base_prices() -> Tuple[Optional[List[Dict]], Optional[str]]:
        return request("GET", "/product_payment/", "No se pudieron obtener los precios")

    @staticmethod
    def price_list(product_id: int) -> Tuple[Optional[Dict], Optional[str]]:
        """Precio final de un producto por método de pago (solo lectura)."""
        return request("GET", f"/product_payment/product/{product_id}/prices",
                       "No se pudo obtener la lista de precios")

    @staticmethod
    def save_base_price(product_id: int, payment_method_id: int,
                        price: float) -> Tuple[Optional[Dict], Optional[str]]:
        """Crea el precio base si el producto no tiene, o lo actualiza si ya tiene."""
        prices, err = ProductService.list_base_prices()
        if err:
            return None, err
        current = next((p for p in prices if p["product_id"] == product_id), None)
        if current is None:
            return request("POST", "/product_payment/", "No se pudo guardar el precio",
                           json={"product_id": product_id, "payment_method_id": payment_method_id,
                                 "price": price})
        return request("PUT", f"/product_payment/{current['product_payment_id']}",
                       "No se pudo actualizar el precio",
                       json={"payment_method_id": payment_method_id, "price": price})

    # ---------- vista agrupada ----------
    @staticmethod
    def load_catalog() -> Tuple[Optional[Dict], Optional[str]]:
        """Carga las tres tablas juntas: cada producto trae su precio base (o None)."""
        products, err = ProductService.list_products()
        if err:
            return None, err
        methods, err = ProductService.list_methods()
        if err:
            return None, err
        prices, err = ProductService.list_base_prices()
        if err:
            return None, err
        by_product = {p["product_id"]: p for p in prices}
        for prod in products:
            base = by_product.get(prod["product_id"])
            prod["base_price"] = base["price"] if base else None
            prod["base_price_id"] = base["product_payment_id"] if base else None
        return {"products": products, "methods": methods}, None