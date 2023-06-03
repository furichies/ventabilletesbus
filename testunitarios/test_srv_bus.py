import unittest
import requests
from bus.srv_bus import app, db, Asiento
from bus.srv_bus import crear_asientos_iniciales


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        with app.app_context():
            db.create_all()
            crear_asientos_iniciales()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_estado_asientos(self):
        with app.app_context():
            response = self.app.get('/asientos')
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data), 44)  # Se asume que hay 44 asientos en la base de datos

    def test_ocupar_asiento(self):
        with app.app_context():
            response = self.app.put('/asientos/ocupar', json={'numero': 1, 'cliente': 'John Doe'})
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['message'], 'Asiento ocupado exitosamente')

            asiento = Asiento.query.filter_by(numero=1).first()
            self.assertEqual(asiento.estado, 'ocupado')
            self.assertEqual(asiento.ocupante, 'John Doe')

    def test_desocupar_asiento(self):
        with app.app_context():
            # Ocupar el asiento primero
            response = self.app.put('/asientos/ocupar', json={'numero': 1, 'cliente': 'John Doe'})
            self.assertEqual(response.status_code, 200)

            response = self.app.put('/asientos/desocupar', json={'numero': 1})
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['message'], 'Asiento desocupado exitosamente')

            asiento = Asiento.query.filter_by(numero=1).first()
            self.assertEqual(asiento.estado, 'libre')
            self.assertEqual(asiento.ocupante, '')

    def test_asientos_libres(self):
        with app.app_context():
            response = self.app.get('/asientos/libres')
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['asientos_libres']), 44)  # Se asume que inicialmente todos los asientos están libres

    def test_asientos_ocupados(self):
        with app.app_context():
            # Ocupar un asiento primero
            response = self.app.put('/asientos/ocupar', json={'numero': 1, 'cliente': 'John Doe'})
            self.assertEqual(response.status_code, 200)

            response = self.app.get('/asientos/ocupados')
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['asientos_ocupados']), 1)
            self.assertEqual(data['asientos_ocupados'][0], 1)

if __name__ == '__main__':
    unittest.main()
