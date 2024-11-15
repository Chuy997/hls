import mysql.connector
from mysql.connector import Error

try:
    # Crear conexión con la base de datos
    connection = mysql.connector.connect(
        host='localhost',  # Este debe ser 'localhost'
        user='root',       # El usuario por defecto es 'root'
        password='',       # Si no configuraste una contraseña, déjalo vacío
        database='hls', 
        port='3306'# La base de datos que creaste
    )

    if connection.is_connected():
        db_info = connection.get_server_info()
        print("Conectado al servidor MySQL versión", db_info)

except Error as e:
    # Mostrar el error específico en detalle
    print("Error al conectar con MySQL:", e)

finally:
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("Conexión con MySQL cerrada")
