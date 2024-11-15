import sys
import os
import subprocess
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def take_screenshots(timestamp):
    rtsp_url = "rtsp://admin:Test.2024@10.232.118.195:554/LiveMedia/ch1/Media1"
    output_dir = "C:/xampp/htdocs/hls/static/alarms"
    
    # Crear la carpeta de salida si no existe
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    screenshots = []
    # Tomar tres capturas de pantalla con FFmpeg, una por segundo
    for i in range(1, 4):
        screenshot_path = os.path.join(output_dir, f"screenshot_{timestamp}_{i}.jpg")
        command = [
            "ffmpeg", "-y", "-i", rtsp_url,
            "-vframes", "1", "-q:v", "2", "-ss", str(i),
            screenshot_path
        ]
        try:
            subprocess.run(command, check=True)
            print(f"Captura de pantalla {i} guardada en {screenshot_path}")
            screenshots.append(screenshot_path)
        except subprocess.CalledProcessError as e:
            print(f"Error al tomar la captura de pantalla {i}: {e}")

    return screenshots

def send_email_with_attachments(screenshots, estado, detalle, fecha):
    # Configuración del servidor SMTP
    smtp_server = "smtp.exmail.qq.com"
    smtp_port = 465
    sender_email = "jesus.muro@zhongli-la.com"
    sender_password = "Chuy.12#$"
    receiver_emails = ["jesus.muro@zhongli-la.com", "cesar.gutierrez@zhongli-la.com"]

    # Crear el mensaje de correo electrónico
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ", ".join(receiver_emails)  # Agregar múltiples destinatarios como una cadena separada por comas
    msg['Subject'] = "Alerta Activada - Registro de Alarma"

    # Cuerpo del mensaje
    body = f"""
    Se ha activado una nueva alarma.

    Estado: {estado}
    Detalle: {detalle}
    Fecha y Hora: {fecha}

    Adjuntamos las capturas de pantalla del evento.
    """
    msg.attach(MIMEText(body, 'plain'))

    # Adjuntar cada screenshot al correo
    for screenshot in screenshots:
        with open(screenshot, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={os.path.basename(screenshot)}",
        )
        msg.attach(part)

    # Conectar al servidor SMTP y enviar el correo
    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(sender_email, sender_password)
        # Enviar el correo a todos los destinatarios al mismo tiempo
        server.sendmail(sender_email, receiver_emails, msg.as_string())
        server.quit()
        print("Correo enviado exitosamente.")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")


if __name__ == "__main__":
    # Obtener los argumentos pasados desde app.py
    estado = sys.argv[1]
    detalle = sys.argv[2]
    fecha = sys.argv[3]

    # Capturar screenshots
    screenshots = take_screenshots(fecha)

    # Enviar correo con los screenshots adjuntos
    send_email_with_attachments(screenshots, estado, detalle, fecha)
