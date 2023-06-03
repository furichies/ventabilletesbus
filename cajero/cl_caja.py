import requests
import json

BASE_URL = "http://localhost:6901"

def make_post_request(endpoint, data):
    headers = {"Content-Type": "application/json"}
    response = requests.post(BASE_URL + endpoint, headers=headers, data=data)
    return response.text

def make_get_request(endpoint):
    response = requests.get(BASE_URL + endpoint)
    return response.text

def registro_usuario():
    nombre = input("Ingrese el nombre: ")
    apellidos = input("Ingrese los apellidos: ")

    data = json.dumps({"nombre": nombre, "apellidos": apellidos})
    response = make_post_request("/registro", data)

    response_data = json.loads(response)
    mensaje = response_data["mensaje"]
    saldo = response_data["saldo"]

    print("Mensaje:", mensaje)
    print("Saldo:", saldo)

def consultar_saldo():
    nombre = input("Ingrese el nombre: ")
    apellidos = input("Ingrese los apellidos: ")

    response = make_get_request("/saldo?nombre=" + nombre + "&apellidos=" + apellidos)
    print("Respuesta recibida:", response)

    response_data = json.loads(response)

    if "mensaje" in response_data:
        mensaje = response_data["mensaje"]
        print("Mensaje:", mensaje)
    else:
        saldo = response_data.get("saldo")
        print("Saldo:", saldo)

def agregar_saldo():
    nombre = input("Ingrese el nombre: ")
    apellidos = input("Ingrese los apellidos: ")
    ingreso = float(input("Ingrese el monto a ingresar: "))

    data = json.dumps({"nombre": nombre, "apellidos": apellidos, "ingreso": ingreso})
    response = make_post_request("/ingreso", data)

    response_data = json.loads(response)
    mensaje = response_data["mensaje"]
    saldo = response_data["saldo"]

    print("Mensaje:", mensaje)
    print("Saldo:", saldo)

def mostrar_menu():
    print("========== MENÚ ==========")
    print("1. Registro de usuario")
    print("2. Consultar saldo")
    print("3. Agregar saldo")
    print("0. Salir")
    print("==========================")

while True:
    mostrar_menu()
    opcion = input("Ingrese una opción: ")
    print()

    if opcion == "1":
        registro_usuario()
    elif opcion == "2":
        consultar_saldo()
    elif opcion == "3":
        agregar_saldo()
    elif opcion == "0":
        break
    else:
        print("Opción inválida. Por favor, seleccione una opción válida.")

    print()

print("¡Hasta luego!")
