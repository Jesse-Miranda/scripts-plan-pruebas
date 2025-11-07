import requests
import unittest
from bs4 import BeautifulSoup


LOGIN_URL = "https://biblioteca-cubo.com/Biblioteca-CUBO/public/user/loginUser"
PERFIL_URL = "https://biblioteca-cubo.com/Biblioteca-CUBO/public/perfil"


class TestPerfilBiblioteca(unittest.TestCase):
    """Pruebas unitarias del módulo de Perfil (Cuadrante 1 - Caja Negra)."""

    @classmethod
    def setUpClass(cls):
        cls.session = requests.Session()
        cls.email = "mp20049@ues.edu.sv"
        cls.password = "12345678"
        print("\n=== Iniciando pruebas del módulo de Perfil ===\n")

        # Iniciar sesión antes de ejecutar las pruebas
        r = cls.session.get(LOGIN_URL)
        soup = BeautifulSoup(r.text, "html.parser")
        token_tag = soup.find("input", {"name": "_token"})
        token = token_tag["value"] if token_tag else None

        payload = {
            "_token": token,
            "email": cls.email,
            "password": cls.password,
        }

        resp = cls.session.post(LOGIN_URL, data=payload, allow_redirects=True)
        assert resp.status_code in [200, 302], "Error al iniciar sesión antes de las pruebas."

    # ----------------------------------------------------------
    # Caso 1: Carga correcta del perfil
    # ----------------------------------------------------------
    def test_carga_perfil_correcta(self):
        r = self.session.get(PERFIL_URL)
        print("\n[Carga de Perfil]")
        print("Status:", r.status_code)
        print("URL:", r.url)

        self.assertEqual(r.status_code, 200)
        self.assertTrue(
            all(x in r.text.lower() for x in ["jesse miranda", "mp20049@ues.edu.sv", "guardar cambios"]),
            "No se encontraron los datos esperados en la vista de perfil."
        )

    # ----------------------------------------------------------
    # Caso 2: Actualización válida de datos
    # ----------------------------------------------------------
    def test_actualizacion_valida(self):
        r = self.session.get(PERFIL_URL)
        soup = BeautifulSoup(r.text, "html.parser")
        token_tag = soup.find("input", {"name": "_token"})
        token = token_tag["value"] if token_tag else None

        payload = {
            "_token": token,
            "_method": "PUT",  # requerido por Laravel
            "nombre": "Jesse Miranda",
            "edad": "25",
            "sexo": "Masculino",
            "correo": self.email,
            "username": "Jesmir",
            "telefono": "79355730",
            "direccion": "Barrio La Cruz, Calle Central",
        }

        resp = self.session.post(PERFIL_URL, data=payload, allow_redirects=True)
        print("\n[Actualización válida]")
        print("Status:", resp.status_code)

        self.assertIn(resp.status_code, [200, 302])
        self.assertTrue(
            any(x in resp.text.lower() for x in ["actualizado", "éxito", "perfil"]),
            "No se detectó mensaje o redirección de éxito."
        )

    # ----------------------------------------------------------
    # Caso 3: Error de validación (edad no numérica)
    # ----------------------------------------------------------
    def test_actualizacion_invalida(self):
        r = self.session.get(PERFIL_URL)
        soup = BeautifulSoup(r.text, "html.parser")
        token_tag = soup.find("input", {"name": "_token"})
        token = token_tag["value"] if token_tag else None

        payload = {
            "_token": token,
            "_method": "PUT",
            "nombre": "Jesse Miranda",
            "edad": "texto",
            "sexo": "Masculino",
            "correo": self.email,
            "username": "Jesmir",
            "telefono": "79355730",
            "direccion": "Barrio inválido",
        }

        resp = self.session.post(PERFIL_URL, data=payload)
        print("\n[Actualización inválida]")
        print("Status:", resp.status_code)

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(
            any(x in resp.text.lower() for x in ["error", "válido", "edad"]),
            "El sistema no mostró error de validación ante dato incorrecto."
        )

    @classmethod
    def tearDownClass(cls):
        print("\n=== Fin de pruebas del módulo de Perfil ===\n")


if __name__ == "__main__":
    unittest.main()