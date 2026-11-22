"""
/app/routes/search_route.py
URL central de búsquedas: /search/customer, /search/product, /search/ingredient.
"""
import sqlite3

from fastapi import APIRouter, Depends

from app.controllers.search_controller import SearchController
from app.database import get_db_connection
from app.views.search_schema import CustomerSearchResponse, ProductSearchResponse

router = APIRouter(prefix="/search", tags=["Search"])


@router.get("/customer", response_model=CustomerSearchResponse)
def search_customer(email: str, db: sqlite3.Connection = Depends(get_db_connection)):
    return SearchController.customer_by_email(db, email)


@router.get("/product", response_model=ProductSearchResponse)
def search_product(q: str, db: sqlite3.Connection = Depends(get_db_connection)):
    return SearchController.products(db, q)


@router.get("/ingredient", response_model=ProductSearchResponse)
def search_ingredient(q: str, db: sqlite3.Connection = Depends(get_db_connection)):
    return SearchController.ingredient(db, q)