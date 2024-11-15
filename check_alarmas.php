<?php
$servername = "localhost"; // Cambia si el servidor es remoto
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

// Insertar datos en la tabla
$sql = "INSERT INTO alarmas (estado, detalle) VALUES ('$estado', '$detalle')";

if ($conn->query($sql) === TRUE) {
    echo "Registro insertado correctamente";
} else {
    echo "Error: " . $sql . "<br>" . $conn->error;
}

$conn->close();
?>