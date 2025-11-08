import requests  # Importa la librería para hacer solicitudes HTTP.
import unittest  # Importa la librería para realizar pruebas unitarias.
from bs4 import BeautifulSoup  # Importa BeautifulSoup para parsear y manipular HTML.
import random  # Importa la librería random para generar datos aleatorios en las pruebas.

# URL base del formulario de registro de usuarios
BASE_URL = "https://biblioteca-cubo.com/Biblioteca-CUBO/public/user/registerUser"

class TestRegistroBiblioteca(unittest.TestCase):
    # Prueba unitaria que valida el flujo completo del módulo de registro de usuarios.
    
    @classmethod
    def setUpClass(cls):
        # Método de configuración que se ejecuta una vez antes de todas las pruebas.
        cls.session = requests.Session()  # Crea una nueva sesión para mantener las cookies entre solicitudes.
        print("\n=== INICIANDO PRUEBAS DE REGISTRO===\n")

    def get_csrf_token(self):
        # Obtiene el token CSRF desde el formulario HTML para prevenir ataques CSRF.
        r = self.session.get(BASE_URL)  # Enviar una solicitud GET a la URL del formulario de registro.
        soup = BeautifulSoup(r.text, "html.parser")  # Utilizar BeautifulSoup para analizar el HTML de la página.
        
        token_tag = soup.find("input", {"name": "_token"})  # Buscar el campo de entrada con el nombre "_token" que contiene el valor CSRF.
        
        # Retornar el valor del token CSRF si se encuentra; de lo contrario, retornar None.
        return token_tag["value"] if token_tag else None

    # ----------------------------------------------------------
    # Caso 1: Registro exitoso (flujo real)
    # ----------------------------------------------------------
    def test_registro_exitoso(self):
        # Prueba unitaria para el registro de usuario con datos válidos y exitosos.
        token = self.get_csrf_token()  # Obtener el token CSRF antes de enviar el formulario.
        self.assertIsNotNone(token, "No se encontró el token CSRF.")  # Verificar que se obtuvo el token CSRF.

        correo_prueba = f"usuario_test_{random.randint(1000,9999)}@example.com"  # Crear un correo aleatorio para este registro de prueba.

        # Crear el payload del formulario con los datos de prueba.
        payload = {
            "_token": token,
            "nombre": "Jesse Miranda",  # Nombre del usuario.
            "edad": "24",               # Edad del usuario.
            "sexo": "Masculino",        # Sexo del usuario.
            "correo": correo_prueba,    # Correo electrónico generado aleatoriamente.
            "username": f"jesmir{random.randint(100,999)}",  # Nombre de usuario único.
            "telefono": "79356730",     # Teléfono del usuario.
            "direccion": "Barrio La Cruz, Calle Principal",  # Dirección del usuario.
            "password": "12345678",     # Contraseña.
            "password_confirmation": "12345678"  # Confirmación de contraseña.
        }

        r = self.session.post(BASE_URL, data=payload, allow_redirects=True)  # Enviar el formulario de registro utilizando POST.

        # Mostrar el estado de la respuesta y la URL final.
        print("\n[Registro exitoso]")
        print("Status:", r.status_code)
        print("URL final:", r.url)

        # Verificar que la respuesta HTTP sea 200 (OK) o 302 (Redirección).
        self.assertIn(r.status_code, [200, 302])

        # Verificar que el texto de la respuesta indique que el usuario está logueado correctamente.
        self.assertTrue(
            any(x in r.text.lower() for x in ["perfil", "cerrar sesión", "biblioteca cubo"]),
            "No se detectó inicio de sesión tras registro."
        )

    # ----------------------------------------------------------
    # Caso 2: Error de validación – contraseñas diferentes
    # ----------------------------------------------------------
    def test_registro_contrasena_invalida(self):
        # Prueba unitaria para verificar el error de validación cuando las contraseñas no coinciden.
        token = self.get_csrf_token()  # Obtener el token CSRF para este caso.

        # Crear un payload con contraseñas que no coinciden.
        payload = {
            "_token": token,
            "nombre": "Error Contraseña",  # Nombre del usuario con error.
            "edad": "22",                  # Edad.
            "sexo": "Femenino",            # Sexo.
            "correo": f"fail_{random.randint(1000,9999)}@example.com",  # Correo de prueba.
            "username": f"userfail{random.randint(100,999)}",  # Nombre de usuario único.
            "telefono": "70001111",        # Teléfono.
            "direccion": "San Miguel",     # Dirección.
            "password": "12345678",        # Contraseña.
            "password_confirmation": "87654321"  # Contraseña de confirmación no coincide.
        }

        r = self.session.post(BASE_URL, data=payload)  # Enviar el formulario y capturar la respuesta.

        print("\n[Contraseñas diferentes]")
        print("Status:", r.status_code)

        # Verificar que la respuesta sea 200 (OK) y que el mensaje de error por contraseñas diferentes esté presente.
        self.assertEqual(r.status_code, 200)
        self.assertIn("contraseña", r.text.lower())

    # ----------------------------------------------------------
    # Caso 3: Error – correo duplicado
    # ----------------------------------------------------------
    def test_registro_correo_duplicado(self):
        # Prueba unitaria para verificar el error de correo duplicado durante el registro.
        token = self.get_csrf_token()  # Obtener el token CSRF para este caso.

        # Crear un payload con un correo que ya existe en la base de datos.
        payload = {
            "_token": token,
            "nombre": "Usuario Duplicado",  # Nombre.
            "edad": "23",                   # Edad.
            "sexo": "Masculino",             # Sexo.
            "correo": "mp20049@ues.edu.sv",  # Correo duplicado.
            "username": "jesmir_duplicado",  # Nombre de usuario.
            "telefono": "79998888",          # Teléfono.
            "direccion": "San Miguel",       # Dirección.
            "password": "12345678",          # Contraseña.
            "password_confirmation": "12345678"  # Confirmación de contraseña.
        }

        r = self.session.post(BASE_URL, data=payload)  # Enviar el formulario y capturar la respuesta.

        print("\n[Correo duplicado]")
        print("Status:", r.status_code)

        # Verificar que la respuesta sea 200 (OK) y que el error de correo duplicado esté presente.
        self.assertEqual(r.status_code, 200)
        self.assertIn("correo", r.text.lower())

    @classmethod
    def tearDownClass(cls):
        # Método de limpieza que se ejecuta una vez después de todas las pruebas.
        print("\n\n=== PRUEBAS DE REGISTRO FINALIZADAS ===\n")

# Ejecutar las pruebas cuando este script es ejecutado directamente.
if __name__ == "__main__":
    unittest.main()
