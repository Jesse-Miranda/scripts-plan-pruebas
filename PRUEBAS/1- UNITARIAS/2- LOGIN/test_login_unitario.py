import requests
import unittest
from bs4 import BeautifulSoup

BASE_URL = "https://biblioteca-cubo.com/Biblioteca-CUBO/public/user/loginUser"


class TestLoginBiblioteca(unittest.TestCase):
    """Pruebas unitarias del módulo de Login (Cuadrante 1 - Caja Negra)."""

    @classmethod
    def setUpClass(cls):
        cls.session = requests.Session()
        print("\n=== Iniciando pruebas del módulo de Login ===\n")

    # ----------------------------------------------------------
    # Función para obtener token CSRF del formulario
    # ----------------------------------------------------------
    def get_csrf_token(self):
        r = self.session.get(BASE_URL)
        soup = BeautifulSoup(r.text, "html.parser")
        token_tag = soup.find("input", {"name": "_token"})
        return token_tag["value"] if token_tag else None

    # ----------------------------------------------------------
    # Caso 1: Login correcto (usuario existente)
    # ----------------------------------------------------------
    def test_login_correcto(self):
        token = self.get_csrf_token()
        self.assertIsNotNone(token, "No se encontró token CSRF")

        payload = {
            "_token": token,
            "email": "mp20049@ues.edu.sv",
            "password": "12345678"
        }

        r = self.session.post(BASE_URL, data=payload, allow_redirects=True)

        print("\n[Login Correcto]")
        print("Status:", r.status_code)
        print("URL final:", r.url)

        # Resultado esperado: ingreso a página principal o perfil
        self.assertIn(r.status_code, [200, 302])
        self.assertTrue(
            any(k in r.text.lower() for k in ["perfil", "cerrar sesión", "biblioteca cubo"]),
            "No se detectó inicio de sesión exitoso."
        )

    # ----------------------------------------------------------
    # Caso 2: Contraseña incorrecta
    # ----------------------------------------------------------
    def test_login_contrasena_incorrecta(self):
        token = self.get_csrf_token()

        payload = {
            "_token": token,
            "email": "mp20049@ues.edu.sv",
            "password": "clave_incorrecta"
        }

        r = self.session.post(BASE_URL, data=payload)

        print("\n[Contraseña Incorrecta]")
        print("Status:", r.status_code)
        self.assertEqual(r.status_code, 200)
        self.assertTrue(
            any(x in r.text.lower() for x in ["credenciales", "incorrecta", "error"]),
            "No se mostró mensaje de error para credenciales inválidas."
        )

    # ----------------------------------------------------------
    # Caso 3: Campo vacío
    # ----------------------------------------------------------
    def test_login_campos_vacios(self):
        token = self.get_csrf_token()

        payload = {
            "_token": token,
            "email": "",
            "password": ""
        }

        r = self.session.post(BASE_URL, data=payload)

        print("\n[Campos Vacíos]")
        print("Status:", r.status_code)
        self.assertEqual(r.status_code, 200)
        self.assertTrue(
            any(x in r.text.lower() for x in ["obligatorio", "requerido", "correo"]),
            "No se mostró mensaje de validación para campos vacíos."
        )

    @classmethod
    def tearDownClass(cls):
        print("\n=== Fin de pruebas del módulo de Login ===\n")


if __name__ == "__main__":
    unittest.main()