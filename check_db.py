"""check_db.py - Solo lectura. Uso: python check_db.py"""
import sqlite3

conn = sqlite3.connect("pasteleria.db")
conn.row_factory = sqlite3.Row

def show(title, rows):
    print(f"\n== {title} ==")
    if not rows:
        print("(vacío)")
    for r in rows:
        print(dict(r))

show("Productos", conn.execute("SELECT product_id, name, size, stock, reserved_stock FROM product"))
show("Pedidos", conn.execute("SELECT order_id, customer_id, state, total FROM orders"))
show("Líneas de pedido", conn.execute(
    "SELECT order_detail_id, order_id, product_id, quantity, unit_price, subtotal FROM order_detail"))
show("HUÉRFANOS: líneas cuyo producto no existe", conn.execute("""
    SELECT od.order_detail_id, od.order_id, od.product_id
    FROM order_detail od LEFT JOIN product p ON p.product_id = od.product_id
    WHERE p.product_id IS NULL"""))
show("Chequeo general de claves foráneas", conn.execute("PRAGMA foreign_key_check"))