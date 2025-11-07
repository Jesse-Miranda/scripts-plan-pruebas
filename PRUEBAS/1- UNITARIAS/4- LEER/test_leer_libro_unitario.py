import requests
import unittest
from bs4 import BeautifulSoup


LOGIN_URL = "https://biblioteca-cubo.com/Biblioteca-CUBO/public/user/loginUser"
LEER_URL = "https://biblioteca-cubo.com/Biblioteca-CUBO/public/libros/EP02025/leer"


class TestLeerLibroBiblioteca(unittest.TestCase):
    """Pruebas unitarias del módulo 'Leer Libro' (Cuadrante 1 - Caja Negra)."""

    @classmethod
    def setUpClass(cls):
        cls.session = requests.Session()
        cls.email = "mp20049@ues.edu.sv"
        cls.password = "12345678"
        print("\n=== Iniciando pruebas del módulo 'Leer Libro' ===\n")

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
        assert resp.status_code in [200, 302], "No se pudo iniciar sesión correctamente antes de las pruebas."

    # ----------------------------------------------------------
    # Caso 1: Carga correcta de la vista de lectura
    # ----------------------------------------------------------
    def test_carga_libro_correcta(self):
        r = self.session.get(LEER_URL)
        print("\n[Carga de libro]")
        print("Status:", r.status_code)
        print("URL:", r.url)

        self.assertEqual(r.status_code, 200)
        self.assertTrue(
            all(k in r.text.lower() for k in ["el principito", "capítulo", "página siguiente"]),
            "No se cargó correctamente el contenido del libro."
        )

    # ----------------------------------------------------------
    # Caso 2: Verificar navegación (botones de lectura)
    # ----------------------------------------------------------
    def test_elementos_de_navegacion(self):
        r = self.session.get(LEER_URL)
        soup = BeautifulSoup(r.text, "html.parser")

        botones = [b.get_text(strip=True).lower() for b in soup.find_all("button")]
        print("\n[Elementos de navegación encontrados]:", botones)

        self.assertTrue(any("página siguiente" in b for b in botones))
        self.assertTrue(any("página anterior" in b for b in botones))
        self.assertTrue(any("índice" in b or "justificar" in b or "noche" in b for b in botones))

    # ----------------------------------------------------------
    # Caso 3: Error – libro inexistente
    # ----------------------------------------------------------
    def test_libro_inexistente(self):
        url_erronea = "https://biblioteca-cubo.com/Biblioteca-CUBO/public/libros/ERROR404/leer"
        r = self.session.get(url_erronea)
        print("\n[Libro inexistente]")
        print("Status:", r.status_code)

        # Resultado esperado: error visible o HTTP 404
        self.assertIn(r.status_code, [200, 404])
        self.assertTrue(
            any(k in r.text.lower() for k in ["error", "no encontrado", "libro"]),
            "El sistema no mostró mensaje de error ante libro inexistente."
        )

    @classmethod
    def tearDownClass(cls):
        print("\n=== Fin de pruebas del módulo 'Leer Libro' ===\n")


if __name__ == "__main__":
    unittest.main()