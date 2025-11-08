import requests  # Importa la librería para hacer solicitudes HTTP.
import unittest  # Importa la librería para realizar pruebas unitarias.
from bs4 import BeautifulSoup  # Importa BeautifulSoup para parsear y manipular HTML.

# URL base del formulario de inicio de sesión
BASE_URL = "https://biblioteca-cubo.com/Biblioteca-CUBO/public/user/loginUser"

class TestLoginBiblioteca(unittest.TestCase):
    # Pruebas unitarias del módulo de Login (Cuadrante 1 - Caja Negra).
    
    @classmethod
    def setUpClass(cls):
        # Configuración inicial que se ejecuta una vez antes de todas las pruebas.
        cls.session = requests.Session()  # Crea una nueva sesión para mantener las cookies entre solicitudes.
        print("\n=== INICIANDO PRUEBAS DE LOGIN ===\n")

    # ----------------------------------------------------------
    # Función para obtener token CSRF del formulario
    # ----------------------------------------------------------
    def get_csrf_token(self):
        # Envía una solicitud GET al formulario de login.
        r = self.session.get(BASE_URL)
        
        # Utiliza BeautifulSoup para analizar la respuesta HTML.
        soup = BeautifulSoup(r.text, "html.parser")
        
        # Busca el campo del token CSRF en el formulario.
        token_tag = soup.find("input", {"name": "_token"})
        
        # Retorna el token CSRF si lo encuentra; de lo contrario, retorna None.
        return token_tag["value"] if token_tag else None

    # ----------------------------------------------------------
    # Caso 1: Login correcto (usuario existente)
    # ----------------------------------------------------------
    def test_login_correcto(self):
        # Prueba unitaria para verificar que el login sea exitoso con un usuario existente.
        token = self.get_csrf_token()  # Obtiene el token CSRF antes de enviar el formulario.
        self.assertIsNotNone(token, "No se encontró token CSRF")  # Verifica que se obtuvo el token CSRF.

        # Datos de login válidos.
        payload = {
            "_token": token,
            "email": "mp20049@ues.edu.sv",  # Email válido.
            "password": "12345678"  # Contraseña válida.
        }

        # Envía el formulario de login con los datos.
        r = self.session.post(BASE_URL, data=payload, allow_redirects=True)

        # Muestra el estado de la respuesta y la URL final.
        print("\n[Login Correcto]")
        print("Status:", r.status_code)
        print("URL final:", r.url)

        # Verifica que la respuesta HTTP sea 200 (OK) o 302 (Redirección).
        self.assertIn(r.status_code, [200, 302])

        # Verifica que el texto de la respuesta indique que el usuario está logueado correctamente.
        self.assertTrue(
            any(k in r.text.lower() for k in ["perfil", "cerrar sesión", "biblioteca cubo"]),
            "No se detectó inicio de sesión exitoso."
        )

    # ----------------------------------------------------------
    # Caso 2: Contraseña incorrecta
    # ----------------------------------------------------------
    def test_login_contrasena_incorrecta(self):
        # Prueba unitaria para verificar el error cuando la contraseña es incorrecta.
        token = self.get_csrf_token()  # Obtiene el token CSRF para este caso.

        # Datos de login con contraseña incorrecta.
        payload = {
            "_token": token,
            "email": "mp20049@ues.edu.sv",  # Email válido.
            "password": "clave_incorrecta"  # Contraseña incorrecta.
        }

        # Envía el formulario de login con los datos.
        r = self.session.post(BASE_URL, data=payload)

        # Muestra el estado y la URL de la respuesta.
        print("\n[Contraseña Incorrecta]")
        print("Status:", r.status_code)

        # Verifica que la respuesta sea 200 (OK) y que se muestre un mensaje de error.
        self.assertEqual(r.status_code, 200)
        self.assertTrue(
            any(x in r.text.lower() for x in ["credenciales", "incorrecta", "error"]),
            "No se mostró mensaje de error para credenciales inválidas."
        )

    # ----------------------------------------------------------
    # Caso 3: Campo vacío
    # ----------------------------------------------------------
    def test_login_campos_vacios(self):
        # Prueba unitaria para verificar el error cuando los campos de email y contraseña están vacíos.
        token = self.get_csrf_token()  # Obtiene el token CSRF para este caso.

        # Datos de login con campos vacíos.
        payload = {
            "_token": token,
            "email": "",  # Campo de email vacío.
            "password": ""  # Campo de contraseña vacío.
        }

        # Envía el formulario de login con los datos.
        r = self.session.post(BASE_URL, data=payload)

        # Muestra el estado y la URL de la respuesta.
        print("\n[Campos Vacíos]")
        print("Status:", r.status_code)

        # Verifica que la respuesta sea 200 (OK) y que se muestre un mensaje de validación para los campos vacíos.
        self.assertEqual(r.status_code, 200)
        self.assertTrue(
            any(x in r.text.lower() for x in ["obligatorio", "requerido", "correo"]),
            "No se mostró mensaje de validación para campos vacíos."
        )

    @classmethod
    def tearDownClass(cls):
        # Método de limpieza que se ejecuta una vez después de todas las pruebas.
        print("\n\n=== PRUEBAS DE LOGIN FINALIZADAS ===\n")


if __name__ == "__main__":
    unittest.main()  # Ejecuta las pruebas cuando el script se ejecuta directamente.
