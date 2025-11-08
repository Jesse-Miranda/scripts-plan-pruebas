import requests  # Importa la librería para hacer solicitudes HTTP.
import unittest  # Importa la librería para realizar pruebas unitarias.
from bs4 import BeautifulSoup  # Importa BeautifulSoup para parsear y manipular HTML.

# URL base del formulario de inicio de sesión y la página de perfil
LOGIN_URL = "https://biblioteca-cubo.com/Biblioteca-CUBO/public/user/loginUser"
PERFIL_URL = "https://biblioteca-cubo.com/Biblioteca-CUBO/public/perfil"

class TestPerfilBiblioteca(unittest.TestCase):
    # Pruebas unitarias del módulo de Perfil (Cuadrante 1 - Caja Negra).

    @classmethod
    def setUpClass(cls):
        # Configuración inicial que se ejecuta una vez antes de todas las pruebas.
        cls.session = requests.Session()  # Crea una nueva sesión para mantener las cookies entre solicitudes.
        cls.email = "mp20049@ues.edu.sv"  # Email del usuario para login.
        cls.password = "12345678"  # Contraseña del usuario para login.
        print("\n=== INICIANDO PRUEBAS DE PERFIL ===\n")

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
        assert resp.status_code in [200, 302], "Error al iniciar sesión antes de las pruebas."

    # ----------------------------------------------------------
    # Caso 1: Carga correcta del perfil
    # ----------------------------------------------------------
    def test_carga_perfil_correcta(self):
        # Verifica que la página de perfil cargue correctamente.
        r = self.session.get(PERFIL_URL)  # Realiza una solicitud GET a la página de perfil.
        print("\n[Carga de Perfil]")
        print("Status:", r.status_code)
        print("URL:", r.url)

        # Verifica que la respuesta sea 200 (OK).
        self.assertEqual(r.status_code, 200)

        # Verifica que los datos del perfil se muestren correctamente en la página.
        self.assertTrue(
            all(x in r.text.lower() for x in ["jesse miranda", "mp20049@ues.edu.sv", "guardar cambios"]),
            "No se encontraron los datos esperados en la vista de perfil."
        )

    # ----------------------------------------------------------
    # Caso 2: Actualización válida de datos
    # ----------------------------------------------------------
    def test_actualizacion_valida(self):
        # Verifica que la actualización del perfil sea exitosa con datos válidos.
        r = self.session.get(PERFIL_URL)  # Realiza una solicitud GET para obtener el formulario de perfil.
        soup = BeautifulSoup(r.text, "html.parser")  # Analiza el HTML de la página.
        token_tag = soup.find("input", {"name": "_token"})  # Busca el campo del token CSRF.
        token = token_tag["value"] if token_tag else None  # Obtiene el token CSRF.

        # Crea un payload con los nuevos datos del perfil.
        payload = {
            "_token": token,
            "_method": "PUT",  # Método PUT requerido por Laravel para actualizar.
            "nombre": "Jesse Miranda",
            "edad": "25",  # Nueva edad.
            "sexo": "Masculino",
            "correo": self.email,  # Mismo correo.
            "username": "Jesmir",  # Nuevo nombre de usuario.
            "telefono": "79355730",  # Nuevo teléfono.
            "direccion": "Barrio La Cruz, Calle Central",  # Nueva dirección.
        }

        # Envía la solicitud POST para actualizar los datos del perfil.
        resp = self.session.post(PERFIL_URL, data=payload, allow_redirects=True)
        print("\n[Actualización válida]")
        print("Status:", resp.status_code)

        # Verifica que la respuesta sea 200 (OK) o 302 (Redirección).
        self.assertIn(resp.status_code, [200, 302])

        # Verifica que el sistema haya mostrado un mensaje de éxito o redirección.
        self.assertTrue(
            any(x in resp.text.lower() for x in ["actualizado", "éxito", "perfil"]),
            "No se detectó mensaje o redirección de éxito."
        )

    # ----------------------------------------------------------
    # Caso 3: Error de validación (edad no numérica)
    # ----------------------------------------------------------
    def test_actualizacion_invalida(self):
        # Verifica que se muestre un error de validación si se introduce un valor inválido en el campo "edad".
        r = self.session.get(PERFIL_URL)  # Realiza una solicitud GET para obtener el formulario de perfil.
        soup = BeautifulSoup(r.text, "html.parser")  # Analiza el HTML de la página.
        token_tag = soup.find("input", {"name": "_token"})  # Busca el campo del token CSRF.
        token = token_tag["value"] if token_tag else None  # Obtiene el token CSRF.

        # Crea un payload con un valor inválido en el campo "edad".
        payload = {
            "_token": token,
            "_method": "PUT",  # Método PUT requerido por Laravel.
            "nombre": "Jesse Miranda",
            "edad": "texto",  # Valor inválido en el campo "edad".
            "sexo": "Masculino",
            "correo": self.email,  # Mismo correo.
            "username": "Jesmir",
            "telefono": "79355730",  # Nuevo teléfono.
            "direccion": "Barrio inválido",  # Dirección inválida.
        }

        # Envía la solicitud POST con los datos inválidos.
        resp = self.session.post(PERFIL_URL, data=payload)
        print("\n[Actualización inválida]")
        print("Status:", resp.status_code)

        # Verifica que la respuesta sea 200 (OK).
        self.assertEqual(resp.status_code, 200)

        # Verifica que el sistema haya mostrado un mensaje de error de validación.
        self.assertTrue(
            any(x in resp.text.lower() for x in ["error", "válido", "edad"]),
            "El sistema no mostró error de validación ante dato incorrecto."
        )

    @classmethod
    def tearDownClass(cls):
        # Método de limpieza que se ejecuta una vez después de todas las pruebas.
        print("\n\n=== PRUEBAS DE PERFIL FINALIZADAS ===\n")

# Ejecuta las pruebas cuando el script es ejecutado directamente.
if __name__ == "__main__":
    unittest.main()
