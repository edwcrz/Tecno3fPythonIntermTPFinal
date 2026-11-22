"""
seed.py - Carga inicial vía API (todo pasa por los controllers y sus validaciones).
Requiere el backend levantado:  python main.py
Uso:                            python seed.py
"""
import sys

import requests

BASE_URL = "http://127.0.0.1:8000"   # debe coincidir con main.py y frontend/config.py
TIMEOUT = 5


def api(method: str, path: str, **kwargs) -> requests.Response:
    return requests.request(method, f"{BASE_URL}{path}", timeout=TIMEOUT, **kwargs)


def ensure(list_path: str, exists, create_path: str, payload: dict, label: str) -> dict:
    """Devuelve el registro existente o lo crea."""
    res = api("GET", list_path)
    # res.raise_for_status()
    if not res.ok:
        print(f"✗  {label}: GET {list_path} -> {res.status_code} {res.text}")
        sys.exit(1)
    for item in res.json():
        if exists(item):
            print(f"=  ya existe: {label}")
            return item
    res = api("POST", create_path, json=payload)
    if not res.ok:
        print(f"✗  {label}: {res.status_code} {res.text}")
        sys.exit(1)
    print(f"+  creado:    {label}")
    return res.json()


# ---------- datos ----------
PAYMENT_METHODS = [
    {"method_name": "Efectivo",           "overload": 0.00},
    {"method_name": "Transferencia",      "overload": 0.00},
    {"method_name": "QR Mercado Pago",    "overload": 0.00},
    {"method_name": "Tarjeta de débito",  "overload": 0.05},
    {"method_name": "Tarjeta de crédito", "overload": 0.10},
]

# (producto, precio base). El Brownie NO tiene precio: sirve para probar el rechazo.
PRODUCTS = [
    ({"name": "Crumble cookie", "description": "Cookie con chips de chocolate",
      "size": "Individual", "product_category": "Cookies", "stock": 20}, 2500.0),
    ({"name": "Lemon pie", "description": "Tarta de limón con merengue",
      "size": "Individual", "product_category": "Tortas", "stock": 5}, 9000.0),
    ({"name": "Torta de chocolate", "description": "Torta húmeda de chocolate",
      "size": "Grande", "product_category": "Tortas", "stock": 3}, 28000.0),
    ({"name": "Brownie", "description": "Brownie con nueces",
      "size": "Individual", "product_category": "Brownies", "stock": 10}, None),
]

CUSTOMERS = [
    # 1: completo, puede comprar
    ({"name": "Ana", "surname": "Pérez", "email": "ana@mail.com", "instagram": "@ana.dulces",
      "phone": "+54 11 1234-5678", "age": 30},
     {"address": "Av. Rivadavia 1234, 3B", "locality": "Caseros",
      "province": "Buenos Aires", "country": "Argentina", "postal_code": "B1678"}),
    # 2: sin email, con dirección -> no puede comprar
    ({"name": "Beto", "surname": "Gómez", "instagram": "@beto.g"},
     {"address": "Calle Falsa 123", "locality": "Caseros",
      "province": "Buenos Aires", "country": "Argentina"}),
    # 3: con email, sin dirección -> no puede comprar
    ({"name": "Carla", "surname": "Ruiz", "email": "carla@mail.com"}, None),
]


def main() -> None:
    try:
        api("GET", "/payment_method/")
    except requests.exceptions.ConnectionError:
        print(f"No se pudo conectar con {BASE_URL}. ¿Está levantado el backend?")
        sys.exit(1)

    print("\n== Métodos de pago ==")
    methods = {}
    for data in PAYMENT_METHODS:
        m = ensure("/payment_method/", lambda i, d=data: i["method_name"] == d["method_name"],
                   "/payment_method/", data, data["method_name"])
        methods[m["method_name"]] = m["payment_method_id"]

    print("\n== Productos y precio base ==")
    for product, price in PRODUCTS:
        p = ensure("/product/",
                   lambda i, d=product: i["name"] == d["name"] and i["size"] == d["size"],
                   "/product/", product, f"{product['name']} ({product['size']})")
        if price is not None:
            ensure("/product_payment/", lambda i, pid=p["product_id"]: i["product_id"] == pid,
                   "/product_payment/",
                   {"product_id": p["product_id"], "payment_method_id": methods["Efectivo"],
                    "price": price}, f"precio base de {product['name']}: ${price:,.0f}")

    print("\n== Clientes y direcciones ==")
    for customer, address in CUSTOMERS:
        c = ensure("/customer/", lambda i, d=customer: i["name"] == d["name"]
                   and i.get("surname") == d.get("surname"),
                   "/customer/", customer, f"cliente {customer['name']}")
        if address:
            payload = {**address, "customer_id": c["customer_id"]}
            ensure(f"/customer_address/customer/{c['customer_id']}",
                   lambda i, a=address: i["address"] == a["address"],
                   "/customer_address/", payload, f"dirección de {customer['name']}")

    print("\nListo. Probá en http://127.0.0.1:8000/docs")


if __name__ == "__main__":
    main()