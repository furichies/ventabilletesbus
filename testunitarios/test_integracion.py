import unittest
import json
import requests
import responses

class TestIntegration(unittest.TestCase):
    def test_compra_billete(self):
        # Paso 1: Registro en http://registro:6900/registro
        registro_url = 'http://registro:6900/registro'
        registro_payload = {
            'nombre': 'nombre',
            'apellidos': 'apellido'
        }
        with responses.RequestsMock() as rsps:
            rsps.add(responses.POST, registro_url, json={'token': 'dummy_token'}, status=200)

            registro_response = requests.post(registro_url, json=registro_payload)
            registro_response_data = json.loads(registro_response.text)

            self.assertEqual(registro_response.status_code, 200)
            self.assertEqual(registro_response_data['token'], 'dummy_token')

        # Paso 2: Registro y saldo en http://cajero:6901/registro y http://cajero:6901/ingreso
        cajero_registro_url = 'http://cajero:6901/registro'
        cajero_saldo_url = 'http://cajero:6901/ingreso'
        cajero_payload = {
            'nombre': 'nombre',
            'apellidos': 'apellido'
        }
        cajero_saldo_payload = {
            'nombre': 'nombre',
            'apellidos': 'apellido',
            'saldo': 1000
        }
        with responses.RequestsMock() as rsps:
            rsps.add(responses.POST, cajero_registro_url, status=200)
            rsps.add(responses.POST, cajero_saldo_url, status=200)

            cajero_registro_response = requests.post(cajero_registro_url, json=cajero_payload)
            cajero_saldo_response = requests.post(cajero_saldo_url, json=cajero_saldo_payload)

            self.assertEqual(cajero_registro_response.status_code, 200)
            self.assertEqual(cajero_saldo_response.status_code, 200)

        # Paso 3: Compra de billete en http://tienda:8888/comprar
        tienda_comprar_url = 'http://tienda:8888/comprar'
        tienda_payload = {
            'nombre': 'nombre',
            'token': 'dummy_token'
        }
        with responses.RequestsMock() as rsps:
            rsps.add(responses.POST, tienda_comprar_url, status=200)

            tienda_response = requests.post(tienda_comprar_url, json=tienda_payload)

            self.assertEqual(tienda_response.status_code, 200)
