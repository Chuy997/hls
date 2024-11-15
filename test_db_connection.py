import mysql.connector
from config import Config

def test_database_connection():
    try:
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB
        )
        if conn.is_connected():
            print("Conexión a la base de datos exitosa.")
        else:
            print("No se pudo conectar a la base de datos.")
    except mysql.connector.Error as err:
        print("Error de conexión:", err)
    finally:
        if conn.is_connected():
            conn.close()
            print("Conexión cerrada.")

if __name__ == "__main__":
    test_database_connection()
