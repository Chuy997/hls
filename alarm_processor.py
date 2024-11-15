import os
import ffmpeg
from datetime import datetime

def process_alarm(estado, detalle, fecha):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = f"static/alarms/{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    
    # Ruta del stream RTSP
    rtsp_url = "rtsp://admin:Test.2024@10.232.118.195:554/LiveMedia/ch1/Media1"
    
    # Crear un segmento de 20 segundos de video
    video_path = os.path.join(output_dir, f"video_alarma_{timestamp}.mp4")
    ffmpeg.input(rtsp_url).output(video_path, t=20, vcodec='libx264', acodec='aac').run()
    
    # Generar screenshots
    screenshots = []
    for i in range(1, 4):
        screenshot_path = os.path.join(output_dir, f"screenshot_{i}.jpg")
        ffmpeg.input(rtsp_url, ss=i).output(screenshot_path, vframes=1).run()
        screenshots.append(screenshot_path)
            
    return {
        "estado": estado,
        "detalle": detalle,
        "fecha": fecha,
        "screenshots": screenshots
    }
