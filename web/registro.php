<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Registro de Usuario</title>
    <style>
        body {
            font-family: "Lucida Console", Monaco, monospace;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(to bottom, #e0e0e0, #ffffff);
            border-radius: 10px;
            margin-top: 100px;
        }

        .button {
            display: inline-block;
            padding: 10px 20px;
            background-color: #333;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            margin-right: 10px;
        }

        .button:hover {
            background-color: #1aa;
        }

        .form-group {
            margin-bottom: 10px;
        }

        .form-group label {
            display: block;
            font-weight: bold;
        }

        .form-group input {
            width: 100%;
            padding: 5px;
            border-radius: 3px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Sociedad cooperativa CBA. Compra de billetes de autobús</h2>
        <form id="registroForm">
            <div class="form-group">
                <label for="nombre">Nombre:</label>
                <input type="text" id="nombre" name="nombre" required>
            </div>
            <div class="form-group">
                <label for="apellidos">Apellidos:</label>
                <input type="text" id="apellidos" name="apellidos" required>
            </div>
            <button class="button" type="submit">Registrar usuario</button>
        </form>
        <button class="button" onclick="mostrarUsuarios()">Obtener usuarios</button>
        <button class="button" onclick="mostrarTokens()">Obtener tokens</button>
        <button class="button" onclick="mostrarBaseDatos()">Obtener base de datos</button>
    </div>

    <script>
        function makeGetRequest(endpoint) {
            var BASE_URL = "http://localhost:6900";
            var xhr = new XMLHttpRequest();
            xhr.open("GET", BASE_URL + endpoint, true);
            xhr.onreadystatechange = function() {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    var response = JSON.parse(xhr.responseText);
                    var formattedResponse = JSON.stringify(response, null, 4);
                    window.alert(formattedResponse);
                }
            };
            xhr.send();
        }

        function registrarUsuario(event) {
            event.preventDefault();

            var BASE_URL = "http://localhost:6900";
            var xhr = new XMLHttpRequest();
            xhr.open("POST", BASE_URL + "/registro", true);
            xhr.setRequestHeader("Content-Type", "application/json");

            var nombre = document.getElementById("nombre").value;
            var apellidos = document.getElementById("apellidos").value;
            var data = JSON.stringify({ "nombre": nombre, "apellidos": apellidos });

            xhr.onreadystatechange = function() {
                if (xhr.readyState === 4) {
                    if (xhr.status === 201) {
                        var response = JSON.parse(xhr.responseText);
                        window.alert("Usuario registrado. Token: " + response.token);
                    } else {
                        window.alert("Error al registrar el usuario.");
                    }
                }
            };

            xhr.send(data);
        }

        function mostrarUsuarios() {
            makeGetRequest("/usuarios");
        }

        function mostrarTokens() {
            makeGetRequest("/tokens");
        }

        function mostrarBaseDatos() {
            makeGetRequest("/basedatos");
        }

        document.getElementById("registroForm").addEventListener("submit", registrarUsuario);
    </script>
</body>
</html>
