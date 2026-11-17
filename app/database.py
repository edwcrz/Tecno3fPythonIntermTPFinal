import sqlite3
from typing import Generator
#   """ Control del flujo de ejecución: Cuando una función ejecuta un yield, 
#   devuelve un valor y suspende temporalmente su ejecución, manteniendo su estado interno intacto. 
#   Cuando el programa vuelve a pedirle otro valor, se reanuda exactamente desde el punto donde se pausó."""

DB_NAME = "pasteleria.db"

def get_db_connection() -> Generator[sqlite3.Connection, None, None]:
#   """ devuelve un generador que produce una conexión a la base de datos SQLite.
#   La conexión se establece con la base de datos especificada por DB_NAME."""
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
#   """ connect a la base de datos SQLite especificada por DB_NAME.
#   El parámetro check_same_thread=False permite que la conexión se comparta entre diferentes hilos de ejecución, 
#   lo que puede ser útil en aplicaciones multihilo."""
    conn.row_factory = sqlite3.Row
#   """ toman los registros y los convierten en objetos para trabajar con por clave, es decir, en lugar de acceder a los valores de las columnas por índice,
#   se puede acceder a ellos por nombre de columna, lo que hace que el código sea más legible y fácil de mantener.
#   Establece que los indices de las tuplas para convertir en un objeto y que para que las consultas devuelvan diccionarios."""
    conn.execute("PRAGMA foreign_keys = ON;")
#   """ excecute("PRAGMA foreign_keys = ON;") habilita el soporte de claves foráneas en SQLite, 
#   lo que permite definir relaciones entre tablas y garantizar la integridad referencial.
#   cuando las tablas estan relaconadas, se puede garantizar que los datos en una tabla estén relacionados con los datos en otra tabla.
#   pragma mantiene la integridad de los datos y evita inconsistencias en la base de datos."""
    try:
        yield conn
#   """ yield conn suspende la ejecución de la función y devuelve la conexión a la base de datos al llamador.
#   Esto permite que el llamador use la conexión para realizar operaciones en la base de datos.
#   Cuando el llamador termina de usar la conexión, puede reanudar la ejecución de la función desde donde se suspendió."""
    finally:
        conn.close()
#   """ finally: garantiza que la conexión a la base de datos se cierre correctamente
#   cuando la función termine de ejecutarse, independientemente de si se produjo una excepción o no.
#   Esto es importante para liberar recursos y evitar fugas de memoria."""

def init_db() -> None:
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS product (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NULL,
                ingredients TEXT NULL,
                taste TEXT NULL,
                texture TEXT NULL,
                size TEXT NULL,
                product_category TEXT NULL,
                product_subcategory TEXT NULL,
                product_group TEXT NULL,
                product_subgroup TEXT NULL,
                stock INTEGER NOT NULL DEFAULT 0);
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS payment_method (
                payment_method_id INTEGER PRIMARY KEY AUTOINCREMENT,
                method_name TEXT NOT NULL DEFAULT "Mercado Pago",
                payment_category TEXT NULL,
                overload INTEGER NOT NULL DEFAULT 0,
                payment_term decimal(10, 2) NOT NULL DEFAULT 0.00,
                subcategory TEXT NULL);
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS product_payment (
                product_payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                payment_method_id INTEGER NOT NULL,
                price DECIMAL(10, 2) NOT NULL DEFAULT 0.01,
                currency TEXT NULL DEFAULT "Pesos",
                FOREIGN KEY (product_id) REFERENCES product (product_id) ON DELETE RESTRICT,
                FOREIGN KEY (payment_method_id) REFERENCES payment_method (payment_method_id) ON DELETE RESTRICT);
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customer (
                customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                nickname TEXT NULL,
                surname TEXT NULL,
                email TEXT NULL,
                instagram TEXT NULL,
                phone TEXT NULL,
                age TEXT NULL,
                gender TEXT NULL,
                likes INTEGER NULL DEFAULT 0,
                notes TEXT NULL);   
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customer_address (
                address_id INTEGER PRIMARY KEY AUTOINCREMENT,
                address TEXT NOT NULL,
                locality TEXT NULL,
                province TEXT NULL,
                pais TEXT NULL,
                postal_code TEXT NULL,
                notes TEXT NULL,
                customer_id INTEGER NOT NULL,
                FOREIGN KEY (customer_id) REFERENCES customer (customer_id) ON DELETE RESTRICT);
        """)
                
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                quantity INTEGER NOT NULL DEFAULT 0,
                state TEXT NOT NULL DEFAULT 'pending',
                communication TEXT NULL,
                FOREIGN KEY (customer_id) REFERENCES customer (customer_id) ON DELETE RESTRICT);
        """)
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS order_detail (
                    order_detail_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    unit_price REAL NOT NULL,
                    FOREIGN KEY (order_id) REFERENCES orders (order_id) ON DELETE CASCADE,
                    FOREIGN KEY (product_id) REFERENCES product (product_id) ON DELETE RESTRICT
                )
            """)
        conn.commit()

if __name__ == "__main__":
    init_db()
    print("Base de datos y tablas creadas correctamente.")
    
