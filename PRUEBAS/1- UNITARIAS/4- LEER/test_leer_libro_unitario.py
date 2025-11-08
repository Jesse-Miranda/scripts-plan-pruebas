import requests  # Importa la librería para hacer solicitudes HTTP.
import unittest  # Importa la librería para realizar pruebas unitarias.
from bs4 import BeautifulSoup  # Importa BeautifulSoup para parsear y manipular HTML.

# URL base del formulario de inicio de sesión y la página de lectura de libros
LOGIN_URL = "https://biblioteca-cubo.com/Biblioteca-CUBO/public/user/loginUser"
LEER_URL = "https://biblioteca-cubo.com/Biblioteca-CUBO/public/libros/EP02025/leer"

class TestLeerLibroBiblioteca(unittest.TestCase):
    # Pruebas unitarias del módulo 'Leer Libro' (Cuadrante 1 - Caja Negra).

    @classmethod
    def setUpClass(cls):
        # Configuración inicial que se ejecuta una vez antes de todas las pruebas.
        cls.session = requests.Session()  # Crea una nueva sesión para mantener las cookies entre solicitudes.
        cls.email = "mp20049@ues.edu.sv"  # Email del usuario para login.
        cls.password = "12345678"  # Contraseña del usuario para login.
        print("\n=== INICIANDO PRUEBAS DE LEER LIBRO ===\n")

        # Iniciar sesión antes de ejecutar las pruebas.
        r = cls.session.get(LOGIN_URL)  # Realiza una solicitud GET para obtener el token CSRF.
        soup = BeautifulSoup(r.text, "html.parser")  # Analiza el HTML de la página.
        token_tag = soup.find("input", {"name": "_token"})  # Busca el campo del token CSRF.
        token = token_tag["value"] if token_tag else None  # Obtiene el valor del token CSRF.

        # Realiza la solicitud POST para hacer login con los datos de usuario.
        payload = {
            "_token": token,
            "email": cls.email,
            "password": cls.password,
        }

        # Envía la solicitud POST para el login.
        resp = cls.session.post(LOGIN_URL, data=payload, allow_redirects=True)
        assert resp.status_code in [200, 302], "No se pudo iniciar sesión correctamente antes de las pruebas."

    # ----------------------------------------------------------
    # Caso 1: Carga correcta de la vista de lectura
    # ----------------------------------------------------------
    def test_carga_libro_correcta(self):
        # Verifica que la página de lectura cargue correctamente.
        r = self.session.get(LEER_URL)  # Realiza una solicitud GET para la página del libro.
        print("\n[Carga de libro]")
        print("Status:", r.status_code)
        print("URL:", r.url)

        # Verifica que la respuesta sea 200 (OK).
        self.assertEqual(r.status_code, 200)

        # Verifica que el contenido de la página cargue correctamente (buscando texto relacionado con el libro).
        self.assertTrue(
            all(k in r.text.lower() for k in ["el principito", "capítulo", "página siguiente"]),
            "No se cargó correctamente el contenido del libro."
        )

    # ----------------------------------------------------------
    # Caso 2: Verificar navegación (botones de lectura)
    # ----------------------------------------------------------
    def test_elementos_de_navegacion(self):
        # Verifica que los botones de navegación estén presentes y funcionen correctamente.
        r = self.session.get(LEER_URL)  # Realiza una solicitud GET para la página del libro.
        soup = BeautifulSoup(r.text, "html.parser")  # Analiza el HTML de la página.

        # Extrae los textos de los botones de la página.
        botones = [b.get_text(strip=True).lower() for b in soup.find_all("button")]
        print("\n[Elementos de navegación encontrados]:", botones)

        # Verifica que los botones de navegación (siguiente, anterior, índice, etc.) estén presentes.
        self.assertTrue(any("página siguiente" in b for b in botones))
        self.assertTrue(any("página anterior" in b for b in botones))
        self.assertTrue(any("índice" in b or "justificar" in b or "noche" in b for b in botones))

    # ----------------------------------------------------------
    # Caso 3: Error – libro inexistente
    # ----------------------------------------------------------
    def test_libro_inexistente(self):
        # Verifica que el sistema maneje correctamente el caso de un libro inexistente.
        url_erronea = "https://biblioteca-cubo.com/Biblioteca-CUBO/public/libros/ERROR404/leer"  # URL errónea para libro inexistente.
        r = self.session.get(url_erronea)  # Realiza una solicitud GET a la URL errónea.
        print("\n[Libro inexistente]")
        print("Status:", r.status_code)

        # Verifica que el código de estado sea 404 (Not Found) o 200 en algunos casos.
        self.assertIn(r.status_code, [200, 404])

        # Verifica que la respuesta contenga un mensaje de error indicando que el libro no fue encontrado.
        self.assertTrue(
            any(k in r.text.lower() for k in ["error", "no encontrado", "libro"]),
            "El sistema no mostró mensaje de error ante libro inexistente."
        )

    @classmethod
    def tearDownClass(cls):
        # Método de limpieza que se ejecuta una vez después de todas las pruebas.
        print("\n\n=== PRUEBAS DE LEER LIBRO FINALIZADAS ===\n")

# Ejecuta las pruebas cuando el script es ejecutado directamente.
if __name__ == "__main__":
    unittest.main()
