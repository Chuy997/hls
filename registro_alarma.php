<?php
date_default_timezone_set('America/Mexico_City'); // Ajuste de zona horaria

// Configuración de la base de datos
$servername = "localhost";
$username = "root";
$password = "Huawei.123";
$dbname = "hls";

// Crear conexión
$conn = new mysqli($servername, $username, $password, $dbname);

// Verificar conexión
if ($conn->connect_error) {
    die("Error de conexión: " . $conn->connect_error);
}

// Obtener datos de la solicitud POST
$estado = $_POST['estado'];
$detalle = $_POST['detalle'];
$fecha = date("Y-m-d H:i:s"); // Obtener la fecha y hora actual

// Insertar datos en la tabla
$sql = "INSERT INTO alarmas (estado, detalle, fecha) VALUES ('$estado', '$detalle', '$fecha')";

if ($conn->query($sql) === TRUE) {
    echo "Registro insertado correctamente";

    // Ejecutar el archivo .bat cuando se detecta una alarma
    $output = shell_exec("C:\\xampp\\htdocs\\hls\\procesar_alarma.bat");

    // Configuración de archivos y rutas para el correo
    $rtsp_url = "rtsp://admin:Test.2024@10.232.118.195:554/LiveMedia/ch1/Media1";
    $timestamp = date("Ymd_His"); // Timestamp para los archivos
    $output_dir = "C:/xampp/htdocs/hls/alarmas/$timestamp";
    if (!file_exists($output_dir)) {
        mkdir($output_dir, 0777, true); // Crear la carpeta de la alarma
    }

    // Crear el segmento de video y screenshots con FFmpeg
    $video_path = "$output_dir/video_alarma_$timestamp.mp4";
    shell_exec("ffmpeg -i $rtsp_url -t 10 -c:v libx264 -c:a aac $video_path");

    // Generar tres capturas de pantalla, una por segundo
    $screenshot1 = "$output_dir/screenshot_1.jpg";
    $screenshot2 = "$output_dir/screenshot_2.jpg";
    $screenshot3 = "$output_dir/screenshot_3.jpg";
    shell_exec("ffmpeg -i $rtsp_url -vframes 1 -ss 1 $screenshot1");
    shell_exec("ffmpeg -i $rtsp_url -vframes 1 -ss 2 $screenshot2");
    shell_exec("ffmpeg -i $rtsp_url -vframes 1 -ss 3 $screenshot3");

    // Preparar el mensaje de correo
    $para = "jesus.muro@zhongli-la.com";
    $asunto = "Alerta Activada - Registro de Alarma";
    $mensaje = "Se ha activado una nueva alarma.\n\n"
             . "Estado: $estado\n"
             . "Detalle: $detalle\n"
             . "Fecha y Hora: $fecha\n\n"
             . "Adjunto encontrarás las capturas de pantalla del evento.";

    // Configuración de encabezados para correo con archivos adjuntos
    $headers = "From: jesus.muro@zhongli-la.com\r\n";
    $headers .= "Bc: cristo.mendoza@huawei.com\r\n";
    $headers .= "MIME-Version: 1.0\r\n";
    $headers .= "Content-Type: multipart/mixed; boundary=\"boundary\"\r\n";

    $message = "--boundary\r\n";
    $message .= "Content-Type: text/plain; charset=UTF-8\r\n\r\n";
    $message .= $mensaje . "\r\n\r\n";

    // Adjuntar cada captura en formato base64
    foreach ([$screenshot1, $screenshot2, $screenshot3] as $index => $screenshot) {
        $file_content = chunk_split(base64_encode(file_get_contents($screenshot)));
        $filename = basename($screenshot);
        $message .= "--boundary\r\n";
        $message .= "Content-Type: image/jpeg; name=\"$filename\"\r\n";
        $message .= "Content-Transfer-Encoding: base64\r\n";
        $message .= "Content-Disposition: attachment; filename=\"$filename\"\r\n\r\n";
        $message .= $file_content . "\r\n\r\n";
    }

    $message .= "--boundary--";

    // Enviar el correo
    if (mail($para, $asunto, $message, $headers)) {
        echo "Correo de aviso enviado correctamente";
    } else {
        echo "Error al enviar el correo de aviso";
    }
} else {
    echo "Error: " . $sql . "<br>" . $conn->error;
}

$conn->close();
