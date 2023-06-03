import unittest
import json
import responses
from flask import Flask
from tienda.tienda import app

class TestComprarBillete(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    @responses.activate
    def test_comprar_billete_exitoso(self):
        data = {
            'nombre': 'ric',
            'token': 'ECjBcmJGeD'
        }

        # Simular la respuesta del endpoint de registro
        responses.add(
            responses.POST,
            'http://registro:6900/verificar',
            json={'existe': True},
            status=200
        )

        # Simular la respuesta del endpoint de plazas
        responses.add(
            responses.GET,
            'http://bus:7000/asientos',
            json={'1': {'estado': 'libre'}, '2': {'estado': 'ocupado'}},
            status=200
        )

        # Simular la respuesta del endpoint de saldo
        responses.add(
            responses.GET,
            'http://cajero:6901/saldo?nombre=ric',
            json={'saldo': 200},
            status=200
        )

        # Simular la respuesta del endpoint de pago
        responses.add(
            responses.POST,
            'http://cajero:6901/pagar',
            json={'mensaje': 'Pago realizado con éxito.'},
            status=200
        )

        # Simular la respuesta del endpoint de ocupar asiento
        responses.add(
            responses.PUT,
            'http://bus:7000/asientos/ocupar',
            json={'message': 'Asiento ocupado exitosamente'},
            status=200
        )

        response = self.app.post('/comprar', json=data)
        response_data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['mensaje'], 'Compra exitosa.')
        self.assertEqual(response_data['asiento'], '1')
        self.assertEqual(response_data['saldo'], 200)

    @responses.activate
    def test_usuario_no_registrado(self):
        data = {
            'nombre': 'No registrado',
            'token': '1234'
        }

        # Simular la respuesta del endpoint de registro
        responses.add(
            responses.POST,
            'http://registro:6900/verificar',
            json={'existe': False},
            status=200
        )

        response = self.app.post('/comprar', json=data)
        response_data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data['mensaje'], 'Usuario no registrado o token incorrecto.')

    @responses.activate
    def test_saldo_insuficiente(self):
        data = {
            'nombre': 'diana',
            'token': 'xRKSCSzNZZ'
        }

        # Simular la respuesta del endpoint de registro
        responses.add(
            responses.POST,
            'http://registro:6900/verificar',
            json={'existe': True},
            status=200
        )

        # Simular la respuesta del endpoint de plazas
        responses.add(
            responses.GET,
            'http://bus:7000/asientos',
            json={'1': {'estado': 'libre'}, '2': {'estado': 'libre'}},
            status=200
        )

        # Simular la respuesta del endpoint de saldo
        responses.add(
            responses.GET,
            'http://cajero:6901/saldo?nombre=diana',
            json={'saldo': 100},
            status=200
        )

        response = self.app.post('/comprar', json=data)
        response_data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_data['mensaje'], 'Saldo insuficiente para comprar el billete.')


if __name__ == '__main__':
    unittest.main()
