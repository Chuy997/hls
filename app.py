from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import datetime, timedelta
import subprocess
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilita CORS para toda la aplicación

# Ruta para la página principal
@app.route('/')
def home():
    return render_template('index.html')

# Ruta para manejar las solicitudes POST desde el ESP32
@app.route('/register_alarm', methods=['POST'])
def register_alarm():
    print("Método de solicitud:", request.method)
    data = request.get_json()  # Recibe la solicitud como JSON

    if not data:
        print("No se recibieron datos.")
        return jsonify({"error": "No se enviaron datos en JSON"}), 400

    estado = data.get('estado')
    detalle = data.get('detalle')
    fecha = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    if estado and detalle:
        print("Alarma recibida: Estado =", estado, "Detalle =", detalle)
        # Guardar alarma en la base de datos SQLite
        if save_alarm_to_db(estado, detalle, fecha):
            # Ejecutar script para capturar screenshots en un proceso separado
            try:
                subprocess.Popen(['python', 'capture_screenshots.py', estado, detalle, fecha])
                print("Script de captura de screenshots ejecutado.")
            except Exception as e:
                print("Error al ejecutar el script de captura de screenshots:", e)

            return jsonify({"message": "Alarma registrada exitosamente"}), 201
        else:
            return jsonify({"error": "Error al guardar la alarma en la base de datos"}), 500
    else:
        print("Error: Datos incompletos.")
        return jsonify({"error": "Datos incompletos"}), 400

@app.route('/get_daily_incidences', methods=['GET'])
def get_daily_incidences():
    try:
        connection = sqlite3.connect('hls_alarms.db')
        cursor = connection.cursor()

        # Generar la lista de fechas de los últimos 7 días
        today = datetime.now().date()
        last_7_days = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]

        # Consulta para obtener el número de incidencias por día
        daily_incidences = {}
        for day in last_7_days:
            cursor.execute("SELECT COUNT(*) FROM alarmas WHERE fecha LIKE ?", (f"{day}%",))
            count = cursor.fetchone()[0]
            daily_incidences[day] = count

        return jsonify(daily_incidences)
    except sqlite3.Error as e:
        print("Error al obtener las incidencias diarias:", e)
        return jsonify({"error": "Error al obtener las incidencias diarias"}), 500
    finally:
        if 'connection' in locals():
            connection.close()

# Ruta para obtener el número total de alarmas registradas
@app.route('/get_alarm_count', methods=['GET'])
def get_alarm_count():
    try:
        # Conectar a la base de datos SQLite
        connection = sqlite3.connect('hls_alarms.db')
        cursor = connection.cursor()

        # Contar el número de incidencias registradas
        cursor.execute('SELECT COUNT(*) FROM alarmas')
        count = cursor.fetchone()[0]

        return jsonify({"count": count})
    except sqlite3.Error as e:
        print("Error al contar las alarmas:", e)
        return jsonify({"error": "Error al contar las alarmas"}), 500
    finally:
        if 'connection' in locals():
            connection.close()
            


def save_alarm_to_db(estado, detalle, fecha):
    try:
        # Conectar a la base de datos SQLite
        connection = sqlite3.connect('hls_alarms.db')
        cursor = connection.cursor()

        # Crear la tabla si no existe
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alarmas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                estado TEXT NOT NULL,
                detalle TEXT NOT NULL,
                fecha TEXT NOT NULL
            )
        ''')

        # Insertar los datos de la alarma
        cursor.execute('''
            INSERT INTO alarmas (estado, detalle, fecha) VALUES (?, ?, ?)
        ''', (estado, detalle, fecha))

        # Confirmar la transacción
        connection.commit()
        print("Alarma guardada en la base de datos con éxito.")
        return True
    except sqlite3.Error as e:
        print("Error al guardar en la base de datos:", e)
        return False
    finally:
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
