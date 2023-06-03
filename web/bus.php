<?php
$BASE_URL = "http://localhost:7000";

function make_get_request($endpoint) {
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $GLOBALS['BASE_URL'] . $endpoint);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $response = curl_exec($ch);
    curl_close($ch);
    return $response;
}

function make_put_request($endpoint, $data) {
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $GLOBALS['BASE_URL'] . $endpoint);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'PUT');
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
    $response = curl_exec($ch);
    curl_close($ch);
    return $response;
}

function get_seat_number() {
    echo "Ingrese el número de asiento: ";
    $seat_number = trim(fgets(STDIN));
    return $seat_number;
}

function get_client_name() {
    echo "Ingrese el nombre del cliente: ";
    $client_name = trim(fgets(STDIN));
    return $client_name;
}

function show_all_seats() {
    echo "Consultando todos los asientos..." . PHP_EOL;
    $response = make_get_request("/asientos");
    echo "Asientos: " . $response . PHP_EOL;
}

function show_available_seats() {
    echo "Consultando asientos libres..." . PHP_EOL;
    $response = make_get_request("/asientos/libres");
    echo "Asientos libres: " . $response . PHP_EOL;
}

function show_occupied_seats() {
    echo "Consultando asientos ocupados..." . PHP_EOL;
    $response = make_get_request("/asientos/ocupados");
    echo "Asientos ocupados: " . $response . PHP_EOL;
}

function occupy_seat() {
    $seat_number = get_seat_number();
    $client_name = get_client_name();
    $data = json_encode(array("numero" => $seat_number, "cliente" => $client_name));

    echo "Ocupando el asiento $seat_number..." . PHP_EOL;
    $response = make_put_request("/asientos/ocupar", $data);
    echo "Respuesta: $response" . PHP_EOL;
}

function release_seat() {
    $seat_number = get_seat_number();
    $data = json_encode(array("numero" => $seat_number));

    echo "Desocupando el asiento $seat_number..." . PHP_EOL;
    $response = make_put_request("/asientos/desocupar", $data);
    echo "Respuesta: $response" . PHP_EOL;
}

while (true) {
    echo "=== Aplicación Cliente de Consulta ===" . PHP_EOL;
    echo "1. Mostrar todos los asientos" . PHP_EOL;
    echo "2. Mostrar asientos libres" . PHP_EOL;
    echo "3. Mostrar asientos ocupados" . PHP_EOL;
    echo "4. Ocupar un asiento" . PHP_EOL;
    echo "5. Desocupar un asiento" . PHP_EOL;
    echo "6. Salir" . PHP_EOL;

    echo "Ingrese una opción: ";
    $choice = trim(fgets(STDIN));

    switch ($choice) {
        case '1':
            show_all_seats();
            break;
        case '2':
            show_available_seats();
            break;
        case '3':
            show_occupied_seats();
            break;
        case '4':
            occupy_seat();
            break;
        case '5':
            release_seat();
            break;
        case '6':
            exit(0);
        default:
            echo "Opción inválida. Inténtelo de nuevo." . PHP_EOL;
    }

    echo PHP_EOL;
}
?>
