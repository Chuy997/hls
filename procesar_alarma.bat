@echo off
setlocal

:: Configuración de variables
set RTSP_URL=rtsp://admin:Test.2024@10.232.118.195:554/LiveMedia/ch1/Media1
set OUTPUT_DIR=C:\xampp\htdocs\hls\alarmas

:: Formatear el timestamp para que sea compatible con nombres de archivo y carpetas
set TIMESTAMP=%date%_%time%
set TIMESTAMP=%TIMESTAMP: =_%
set TIMESTAMP=%TIMESTAMP:/=-%
set TIMESTAMP=%TIMESTAMP::=-%
set TIMESTAMP=%TIMESTAMP:.=-%

:: Crear carpeta de alarmas si no existe
if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

:: Crear carpeta específica para el segmento de video y capturas basadas en el timestamp
set ALARMA_DIR=%OUTPUT_DIR%\%TIMESTAMP%
mkdir "%ALARMA_DIR%"

:: Extraer 10 segundos de video y almacenar en la carpeta de la alarma
ffmpeg -i %RTSP_URL% -t 10 -c:v libx264 -c:a aac "%ALARMA_DIR%\video_alarma_%TIMESTAMP%.mp4"

:: Generar 3 capturas de pantalla, una por segundo durante los primeros 3 segundos del video
ffmpeg -i %RTSP_URL% -vframes 1 -ss 1 "%ALARMA_DIR%\screenshot_1.jpg"
ffmpeg -i %RTSP_URL% -vframes 1 -ss 2 "%ALARMA_DIR%\screenshot_2.jpg"
ffmpeg -i %RTSP_URL% -vframes 1 -ss 3 "%ALARMA_DIR%\screenshot_3.jpg"

echo "Proceso de alarma completado en %ALARMA_DIR%"
endlocal
pause
