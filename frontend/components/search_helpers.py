"""
/frontend/components/search_helpers.py
Funciones sueltas que comparten los formularios con buscador (no hay widget aparte).
"""
from typing import Callable, Dict, List

import customtkinter as ctk

from frontend.config import COLORS


def say(label, text: str, is_error: bool = False):
    label.configure(text=text, text_color=COLORS["status_err"] if is_error else COLORS["status_ok"])


def clear_options(container):
    for widget in container.winfo_children():
        widget.destroy()


def show_options(container, items: List[Dict], label_fn: Callable[[Dict], str],
                 on_pick: Callable[[Dict], None], max_results: int = 8):
    """Muestra los resultados como botones para hacer clic."""
    clear_options(container)
    for item in items[:max_results]:
        ctk.CTkButton(container, text=label_fn(item), anchor="w", height=26,
                      fg_color=COLORS["bg_card"], hover_color=COLORS["cancel"],
                      text_color=("gray10", "gray90"),
                      command=lambda i=item: on_pick(i)).pack(fill="x", pady=2)


def filter_local(items: List[Dict], fields: tuple, text: str) -> List[Dict]:
    """Tipo %texto%: todas las palabras deben aparecer. Texto vacío = todos."""
    words = text.lower().split()
    return [i for i in items
            if all(w in " ".join(str(i.get(f) or "") for f in fields).lower() for w in words)]


def label_customer(c: Dict) -> str:
    return f"#{c['customer_id']} {c['name']} {c.get('surname') or ''} - {c.get('email') or 'sin email'}".strip()


def label_product(p: Dict, show_ingredients: bool = False) -> str:
    base = p.get("base_price")
    price = f"${base:,.2f}" if base is not None else "sin precio"
    text = f"#{p['product_id']} {p['name']} ({p['size']}) - {price} - disp. {p['available']}"
    if show_ingredients and p.get("ingredients"):
        text += f"\n   Ingredientes: {p['ingredients']}"
    return text


def label_method(m: Dict) -> str:
    return f"{m['method_name']} (+{m['overload'] * 100:g}%)"