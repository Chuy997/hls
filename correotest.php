<?php
$para = "jesus.muro@zhongli-la.com";
$asunto = "Prueba de Envío de Correo desde XAMPP";
$mensaje = "¡Hola! Esta es una prueba de que el servicio de correo está funcionando.";
$headers = "From: jesus.muro@zhongli-la.com";

if (mail($para, $asunto, $mensaje, $headers)) {
    echo "Correo enviado exitosamente.";
} else {
    echo "Error al enviar el correo.";
}
?>
