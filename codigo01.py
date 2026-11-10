import sqlite3

def conectar():
    try:
        conexion = sqlite3.connect("estudiantes.db")
        return conexion
    except sqlite3.Error as error:
        print(f"Error al conectar con la base de datos: {error}")
        return None

def cargar_partes():
    conexion = None
    try:
        conexion = conectar()
        if not conexion:
            return {}

        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM vendor")
        registros = cursor.fetchall()

        """
        materias = {}
        for id_materia, nombre in registros:
            materias[id_materia] = nombre"""

        return registros #materias

    except sqlite3.Error as error:
        print(f"Error al consultar materias: {error}")
        return {}
    finally:
        if conexion:
            conexion.close()

partes = cargar_partes()

print(partes)