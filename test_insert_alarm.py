import mysql.connector
from datetime import datetime
from config import Config

def test_insert_alarm():
    estado = "activada"
    detalle = "Detección de alarma de fuego o temperatura alta"
    fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB
        )
        cursor = conn.cursor()
        insert_query = "INSERT INTO alarmas (estado, detalle, fecha) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (estado, detalle, fecha))
        conn.commit()
        print("Alarma registrada correctamente en la base de datos.")
    except mysql.connector.Error as err:
        print("Error al insertar en la base de datos:", err)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("Conexión cerrada.")

if __name__ == "__main__":
    test_insert_alarm()
