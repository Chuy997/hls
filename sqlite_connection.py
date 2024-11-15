import sqlite3
from sqlite3 import Error

try:
    # Conectar a la base de datos SQLite (o crearla si no existe)
    connection = sqlite3.connect('hls_alarms.db')
    print("Conexión a SQLite establecida con éxito")

    # Crear cursor para ejecutar comandos SQL
    cursor = connection.cursor()

    # Crear la tabla para las alarmas si no existe ya
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alarmas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    print("Tabla de alarmas creada o ya existente")

except Error as e:
    print("Error al conectar con SQLite:", e)

finally:
    if connection:
        connection.close()
        print("Conexión con SQLite cerrada")
