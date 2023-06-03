<?php
function make_post_request($endpoint, $data) {
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, "http://localhost:6901" . $endpoint);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
    $response = curl_exec($ch);
    curl_close($ch);
    return $response;
}

function registro_usuario() {
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        $nombre = $_POST['nombre'];
        $apellidos = $_POST['apellidos'];

        $data = array('nombre' => $nombre, 'apellidos' => $apellidos);
        $jsonData = json_encode($data);

        $response = make_post_request('/registro', $jsonData);
        $responseData = json_decode($response, true);

        $mensaje = $responseData['mensaje'];
        $saldo = $responseData['saldo'];

        echo "Mensaje: $mensaje<br>";
        echo "Saldo: $saldo<br>";
    }
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Aplicación Cajero</title>
</head>
<body>
    <h1>Aplicación Cajero</h1>
    <form method="post">
        <label for="nombre">Nombre:</label>
        <input type="text" id="nombre" name="nombre" required><br>
        <label for="apellidos">Apellidos:</label>
        <input type="text" id="apellidos" name="apellidos" required><br>
        <input type="submit" value="Registrar usuario">
    </form>

    <?php registro_usuario(); ?>
</body>
</html>
