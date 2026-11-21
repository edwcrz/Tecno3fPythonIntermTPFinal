"""
/app/controllers/common.py
Validaciones y manejo de transacciones compartidos por todos los controllers.
"""
import re
import sqlite3
from contextlib import contextmanager
from typing import Optional

from fastapi import HTTPException, status

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_RE = re.compile(r"^[0-9+\-\s()]{6,20}$")

def not_found(what: str, item_id) -> HTTPException:
    return HTTPException(status.HTTP_404_NOT_FOUND, f"{what} {item_id} no existe")

def conflict(msg: str) -> HTTPException:
    return HTTPException(status.HTTP_409_CONFLICT, msg)

def invalid(msg: str) -> HTTPException:
    return HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, msg)

def required_text(value, field: str, max_len: int = 100) -> str:
    text = str(value).strip() if value is not None else ""
    if not text:
        raise invalid(f"'{field}' es obligatorio")
    if len(text) > max_len:
        raise invalid(f"'{field}' admite hasta {max_len} caracteres")
    return text

def optional_text(value, field: str, max_len: int = 100) -> Optional[str]:
    text = str(value).strip() if value is not None else ""
    if not text:
        return None
    if len(text) > max_len:
        raise invalid(f"'{field}' admite hasta {max_len} caracteres")
    return text

def positive_int(value, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise invalid(f"'{field}' debe ser un entero mayor a 0")
    return value

def non_negative_int(value, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise invalid(f"'{field}' debe ser un entero mayor o igual a 0")
    return value

@contextmanager
def transaction(db: sqlite3.Connection):
    """Todo o nada: commit si sale bien, rollback si algo falla."""
    try:
        yield
        db.commit()
    except HTTPException:
        db.rollback()
        raise
    except sqlite3.IntegrityError:
        db.rollback()
        raise conflict("Operación rechazada: hay datos relacionados o un valor no permitido")
    except sqlite3.Error as e:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Error de base de datos: {e}")