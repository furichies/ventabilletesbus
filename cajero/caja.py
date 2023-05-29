from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
db = SQLAlchemy(app)


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    saldo = db.Column(db.Float, nullable=False, default=0)


@app.route('/registro', methods=['POST'])
def registro():
    """
    Registra un nuevo usuario.

    :return: Mensaje de éxito o error en formato JSON.
    """
    data = request.get_json()
    nombre = data.get('nombre')
    apellidos = data.get('apellidos')

    usuario_existente = Usuario.query.filter_by(nombre=nombre, apellidos=apellidos).first()
    if usuario_existente:
        return jsonify({'mensaje': 'El usuario ya está registrado.'}), 400

    nuevo_usuario = Usuario(nombre=nombre, apellidos=apellidos, saldo=100)
    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({'mensaje': 'Usuario registrado con éxito.', 'saldo': nuevo_usuario.saldo})


@app.route('/saldo', methods=['GET'])
def consultar_saldo():
    """
    Consulta el saldo de un usuario.

    :return: Saldo del usuario en formato JSON.
    """
    nombre = request.args.get('nombre')
    usuario = Usuario.query.filter_by(nombre=nombre).first()

    if usuario:
        return jsonify({'saldo': usuario.saldo})

    return jsonify({'mensaje': 'Usuario no encontrado.'}), 404


@app.route('/pagar', methods=['POST'])
def realizar_pago():
    """
    Realiza un pago utilizando el saldo de un usuario.

    :return: Mensaje de éxito o error en formato JSON.
    """
    data = request.get_json()
    nombre = data.get('nombre')
    costo = data.get('costo')

    usuario = Usuario.query.filter_by(nombre=nombre).first()

    if usuario:
        if usuario.saldo >= costo:
            usuario.saldo -= costo
            db.session.commit()
            return jsonify({'mensaje': 'Pago realizado con éxito.', 'saldo': usuario.saldo})
        else:
            return jsonify({'mensaje': 'Saldo insuficiente.'}), 400

    return jsonify({'mensaje': 'Usuario no encontrado.'}), 404


@app.route('/ingreso', methods=['POST'])
def agregar_saldo():
    """
    Agrega saldo a un usuario existente.

    :return: Mensaje de éxito o error en formato JSON.
    """
    data = request.get_json()
    nombre = data.get('nombre')
    apellidos = data.get('apellidos')
    ingreso = data.get('ingreso')

    usuario = Usuario.query.filter_by(nombre=nombre, apellidos=apellidos).first()

    if usuario:
        usuario.saldo += ingreso
        db.session.commit()
        return jsonify({'mensaje': 'Ingreso realizado con éxito.', 'saldo': usuario.saldo})

    return jsonify({'mensaje': 'Usuario no encontrado.'}), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=6901)
