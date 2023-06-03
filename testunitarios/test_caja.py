import unittest
import json
from cajero.caja import app, db, Usuario


class CajeroIntegrationTest(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.testing = True
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_registro(self):
        response = self.app.post('/registro', json={'nombre': 'John', 'apellidos': 'Doe'})
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['mensaje'], 'Usuario registrado con éxito.')
        self.assertEqual(data['saldo'], 100)

    def test_consultar_saldo(self):
        usuario = Usuario(nombre='John', apellidos='Doe', saldo=150)
        with app.app_context():
            db.session.add(usuario)
            db.session.commit()

        response = self.app.get('/saldo?nombre=John')
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['saldo'], 150)

    def test_realizar_pago_saldo_suficiente(self):
        usuario = Usuario(nombre='John', apellidos='Doe', saldo=200)
        with app.app_context():
            db.session.add(usuario)
            db.session.commit()

        response = self.app.post('/pagar', json={'nombre': 'John', 'costo': 150})
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['mensaje'], 'Pago realizado con éxito.')
        self.assertEqual(data['saldo'], 50)

    def test_realizar_pago_saldo_insuficiente(self):
        usuario = Usuario(nombre='John', apellidos='Doe', saldo=50)
        with app.app_context():
            db.session.add(usuario)
            db.session.commit()

        response = self.app.post('/pagar', json={'nombre': 'John', 'costo': 100})
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['mensaje'], 'Saldo insuficiente.')

    def test_agregar_saldo(self):
        usuario = Usuario(nombre='John', apellidos='Doe', saldo=100)
        with app.app_context():
            db.session.add(usuario)
            db.session.commit()

        response = self.app.post('/ingreso', json={'nombre': 'John', 'apellidos': 'Doe', 'ingreso': 50})
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['mensaje'], 'Ingreso realizado con éxito.')
        self.assertEqual(data['saldo'], 150)


if __name__ == '__main__':
    unittest.main()
