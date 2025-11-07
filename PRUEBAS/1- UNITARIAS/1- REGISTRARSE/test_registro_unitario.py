import requests
import unittest
from bs4 import BeautifulSoup
import random

BASE_URL = "https://biblioteca-cubo.com/Biblioteca-CUBO/public/user/registerUser"


class TestRegistroBiblioteca(unittest.TestCase):
    """Prueba unitaria real del módulo de registro (Cuadrante 1 - Caja Negra)."""

    @classmethod
    def setUpClass(cls):
        cls.session = requests.Session()
        print("\n=== Iniciando pruebas del módulo de Registro ===\n")

    def get_csrf_token(self):
        """Obtiene el token CSRF desde el formulario HTML."""
        r = self.session.get(BASE_URL)
        soup = BeautifulSoup(r.text, "html.parser")
        token_tag = soup.find("input", {"name": "_token"})
        return token_tag["value"] if token_tag else None

    # ----------------------------------------------------------
    # Caso 1: Registro exitoso (flujo real)
    # ----------------------------------------------------------
    def test_registro_exitoso(self):
        token = self.get_csrf_token()
        self.assertIsNotNone(token, "No se encontró el token CSRF.")

        correo_prueba = f"usuario_test_{random.randint(1000,9999)}@example.com"

        payload = {
            "_token": token,
            "nombre": "Jesse Miranda",
            "edad": "24",
            "sexo": "Masculino",
            "correo": correo_prueba,
            "username": f"jesmir{random.randint(100,999)}",
            "telefono": "79356730",
            "direccion": "Barrio La Cruz, Calle Principal",
            "password": "12345678",
            "password_confirmation": "12345678"
        }

        r = self.session.post(BASE_URL, data=payload, allow_redirects=True)

        print("\n[Registro exitoso]")
        print("Status:", r.status_code)
        print("URL final:", r.url)

        self.assertIn(r.status_code, [200, 302])
        self.assertTrue(
            any(x in r.text.lower() for x in ["perfil", "cerrar sesión", "biblioteca cubo"]),
            "No se detectó inicio de sesión tras registro."
        )

    # ----------------------------------------------------------
    # Caso 2: Error de validación – contraseñas diferentes
    # ----------------------------------------------------------
    def test_registro_contrasena_invalida(self):
        token = self.get_csrf_token()

        payload = {
            "_token": token,
            "nombre": "Error Contraseña",
            "edad": "22",
            "sexo": "Femenino",
            "correo": f"fail_{random.randint(1000,9999)}@example.com",
            "username": f"userfail{random.randint(100,999)}",
            "telefono": "70001111",
            "direccion": "San Miguel",
            "password": "12345678",
            "password_confirmation": "87654321"
        }

        r = self.session.post(BASE_URL, data=payload)
        print("\n[Contraseñas diferentes]")
        print("Status:", r.status_code)
        self.assertEqual(r.status_code, 200)
        self.assertIn("contraseña", r.text.lower())

    # ----------------------------------------------------------
    # Caso 3: Error – correo duplicado
    # ----------------------------------------------------------
    def test_registro_correo_duplicado(self):
        token = self.get_csrf_token()

        payload = {
            "_token": token,
            "nombre": "Usuario Duplicado",
            "edad": "23",
            "sexo": "Masculino",
            "correo": "mp20049@ues.edu.sv",  # correo existente
            "username": "jesmir_duplicado",
            "telefono": "79998888",
            "direccion": "San Miguel",
            "password": "12345678",
            "password_confirmation": "12345678"
        }

        r = self.session.post(BASE_URL, data=payload)
        print("\n[Correo duplicado]")
        print("Status:", r.status_code)
        self.assertEqual(r.status_code, 200)
        self.assertIn("correo", r.text.lower())

    @classmethod
    def tearDownClass(cls):
        print("\n=== Fin de pruebas del módulo de Registro ===\n")


if __name__ == "__main__":
    unittest.main()