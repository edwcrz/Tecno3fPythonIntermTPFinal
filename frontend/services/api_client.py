"""
/frontend/services/api_client.py
Acceso HTTP único: devuelve (datos, error). El error es un texto legible
que incluye el 'detail' que manda el backend.
"""
from typing import Any, Optional, Tuple

import requests

from frontend.config import API_BASE_URL

TIMEOUT = 5


def _error_message(res: requests.Response, default: str) -> str:
    try:
        detail = res.json().get("detail")
    except (ValueError, AttributeError):
        detail = None
    if isinstance(detail, str):
        return detail
    if isinstance(detail, list) and detail:   # errores de validación (422)
        first = detail[0]
        loc = ".".join(str(x) for x in first.get("loc", []) if x != "body")
        return f"{default}: {loc} - {first.get('msg', 'dato inválido')}"
    return f"{default} (error {res.status_code})"


def request(method: str, path: str, default_error: str, **kwargs) -> Tuple[Any, Optional[str]]:
    try:
        res = requests.request(method, f"{API_BASE_URL}{path}", timeout=TIMEOUT, **kwargs)
    except requests.exceptions.ConnectionError:
        return None, "No se pudo conectar con el servidor. ¿Está levantado el backend?"
    except requests.exceptions.Timeout:
        return None, "El servidor tardó demasiado en responder."
    except requests.exceptions.RequestException as e:
        return None, f"Error de red: {e}"

    if not res.ok:
        return None, f"{_error_message(res, default_error)} [{method} {path}]"
    if res.status_code == 204 or not res.content:
        return True, None
    return res.json(), None


def clean(data: dict, fields: tuple) -> dict:
    """Se queda con los campos permitidos y convierte textos vacíos en None."""
    out = {}
    for f in fields:
        value = data.get(f)
        out[f] = value.strip() or None if isinstance(value, str) else value
    return out