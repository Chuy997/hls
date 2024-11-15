import sqlite3

# Crea una conexión y un cursor
connection = sqlite3.connect('hls_alarms.db')
cursor = connection.cursor()

# Crear una tabla si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS alarmas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    estado TEXT NOT NULL,
    detalle TEXT NOT NULL,
    fecha TEXT NOT NULL
)
''')

# Cerrar la conexión
connection.close()

print("Base de datos y tabla creadas correctamente.")
