import sys
import os
import ffmpeg
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import subprocess


def capture_screenshots(estado, detalle, fecha):
    # Ruta del stream RTSP
    rtsp_url = "rtsp://admin:Test.2024@10.232.118.195:554/LiveMedia/ch1/Media1"
    
    # Crear la carpeta para almacenar las capturas
    output_dir = f"C:/xampp/htdocs/hls/static/alarms/{fecha}"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generar tres capturas de pantalla con un segundo de diferencia cada una
    screenshots = []
    for i in range(1, 4):
        screenshot_path = os.path.join(output_dir, f"screenshot_{i}.jpg")
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
    receiver_emails = ["jesus.muro@zhongli-la.com","cristo.mendoza@huawei.com"]

    # Crear el mensaje de correo electrónico
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ", ".join(receiver_emails)  # Agregar múltiples destinatarios como una cadena separada por comas
    msg['Subject'] = "Alerta Activada - Registro de Alarma"

    # Cuerpo del mensaje con HTML
    body_html = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                color: #333;
                line-height: 1.6;
            }}
            .container {{
                width: 80%;
                margin: auto;
                background: #fff;
                padding: 20px;
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
                border-radius: 8px;
            }}
            .header {{
                background-color: #B4182D;
                color: white;
                padding: 10px 0;
                text-align: center;
                font-size: 24px;
                font-weight: bold;
            }}
            .content {{
                margin-top: 20px;
                font-size: 16px;
            }}
            .details {{
                background-color: #f8d7da;
                padding: 15px;
                border-radius: 5px;
                margin-top: 20px;
            }}
            .footer {{
                text-align: center;
                margin-top: 30px;
                font-size: 14px;
                color: #777;
            }}
            .alert-icon {{
                width: 100px;
                height: auto;
                margin: 10px auto;
                display: block;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                🚨 Alerta de Incendio / Humo 🚨
            </div>
            <div class="content">
                <p>Se ha detectado una posible emergencia. A continuación se detallan los datos de la alerta:</p>
                <div class="details">
                    <p><strong>Estado:</strong> {estado}</p>
                    <p><strong>Detalle:</strong> {detalle}</p>
                    <p><strong>Fecha y Hora:</strong> {fecha}</p>
                </div>
                <p>Por favor, revise las capturas de pantalla adjuntas para evaluar la situación y tomar las acciones necesarias.</p>
            </div>
            <div class="footer">
                <p>Este es un mensaje automático generado por el sistema de monitoreo. Por favor, no responda a este correo.</p>
            </div>
        </div>
    </body>
    </html>
    """

    msg.attach(MIMEText(body_html, 'html'))

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
        # Enviar el correo a cada destinatario de manera individual
        for email in receiver_emails:
            server.sendmail(sender_email, email, msg.as_string())
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
    screenshots = capture_screenshots(estado, detalle, fecha)

    # Verificar si se tomaron los screenshots correctamente antes de intentar enviar el correo
    if screenshots:
        send_email_with_attachments(screenshots, estado, detalle, fecha)
    else:
        print("No se tomaron capturas de pantalla. No se enviará el correo.")
