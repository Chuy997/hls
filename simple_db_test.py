import mysql.connector
from mysql.connector import Error

try:
    # Crear conexión con la base de datos
    connection = mysql.connector.connect(
        host='localhost',
        user='root',        # Cambia 'root' si tienes otro usuario configurado
        password='',        # Cambia '' si tienes una contraseña establecida
        database='hls'      # Nuestra base de datos creada
    )

    if connection.is_connected():
        db_info = connection.get_server_info()
        print("Conectado al servidor MySQL versión", db_info)

except Error as e:
    print("Error al conectar con MySQL", e)
finally:
    if connection.is_connected():
        connection.close()
        print("Conexión con MySQL cerrada")
