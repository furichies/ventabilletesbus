from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import requests
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
socketio = SocketIO(app)

BASE_URL = "http://localhost:6901"

def make_post_request(endpoint, data):
    headers = {"Content-Type": "application/json"}
    response = requests.post(BASE_URL + endpoint, headers=headers, data=data)
    return response.text

def make_get_request(endpoint):
    response = requests.get(BASE_URL + endpoint)
    return response.text

@app.route('/registro', methods=['POST'])
def registro_usuario():
    data = request.get_json()
    nombre = data.get("nombre")
    apellidos = data.get("apellidos")

    data = json.dumps({"nombre": nombre, "apellidos": apellidos})
    response = make_post_request("/registro", data)

    response_data = json.loads(response)
    mensaje = response_data["mensaje"]
    saldo = response_data["saldo"]

    return jsonify({"mensaje": mensaje, "saldo": saldo})

@app.route('/saldo', methods=['GET'])
def consultar_saldo():
    nombre = request.args.get("nombre")
    apellidos = request.args.get("apellidos")

    response = make_get_request("/saldo?nombre=" + nombre + "&apellidos=" + apellidos)

    response_data = json.loads(response)

    if "mensaje" in response_data:
        mensaje = response_data["mensaje"]
        return jsonify({"mensaje": mensaje})
    else:
        saldo = response_data.get("saldo")
        return jsonify({"saldo": saldo})

@app.route('/ingreso', methods=['POST'])
def agregar_saldo():
    data = request.get_json()
    nombre = data.get("nombre")
    apellidos = data.get("apellidos")
    ingreso = data.get("ingreso")

    data = json.dumps({"nombre": nombre, "apellidos": apellidos, "ingreso": ingreso})
    response = make_post_request("/ingreso", data)

    response_data = json.loads(response)
    mensaje = response_data["mensaje"]
    saldo = response_data["saldo"]

    return jsonify({"mensaje": mensaje, "saldo": saldo})

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('registro_usuario')
def handle_registro_usuario(data):
    nombre = data.get('nombre')
    apellidos = data.get('apellidos')

    print(f"Recibido evento 'registro_usuario' con datos: nombre={nombre}, apellidos={apellidos}")

    data = json.dumps({"nombre": nombre, "apellidos": apellidos})
    response = make_post_request("/registro", data)

    response_data = json.loads(response)
    mensaje = response_data["mensaje"]
    saldo = response_data["saldo"]

    # Emitir el evento 'registro_usuario_respuesta' al cliente con el resultado del registro
    emit('registro_usuario_respuesta', {'mensaje': mensaje, 'saldo': saldo})


@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
