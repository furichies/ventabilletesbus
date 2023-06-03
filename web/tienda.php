<?php
function make_get_request($endpoint) {
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, "http://localhost:6900" . $endpoint);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $response = curl_exec($ch);
    curl_close($ch);
    return $response;
}

function obtener_usuarios() {
    $response = make_get_request('/usuarios');
    echo "Usuarios: $response";
}

function obtener_tokens() {
    $response = make_get_request('/tokens');
    echo "Tokens: $response";
}

function obtener_basedatos() {
    $response = make_get_request('/basedatos');
    echo "Base de datos: $response";
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Aplicación Tienda</title>
</head>
<body>
    <h1>Aplicación Tienda</h1>
    <button onclick="obtenerUsuarios()">Obtener usuarios</button>
    <button onclick="obtenerTokens()">Obtener tokens</button>
    <button onclick="obtenerBaseDatos()">Obtener base de datos</button>

    <script>
        function obtenerUsuarios() {
            fetch('http://localhost:8080/api/tienda/usuarios')
                .then(response => response.json())
                .then(data => {
                    alert("Usuarios: " + JSON.stringify(data));
                });
        }

        function obtenerTokens() {
            fetch('http://localhost:8080/api/tienda/tokens')
                .then(response => response.json())
                .then(data => {
                    alert("Tokens: " + JSON.stringify(data));
                });
        }

        function obtenerBaseDatos() {
            fetch('http://localhost:8080/api/tienda/basedatos')
                .then(response => response.json())
                .then(data => {
                    alert("Base de datos: " + JSON.stringify(data));
                });
        }
    </script>
</body>
</html>
