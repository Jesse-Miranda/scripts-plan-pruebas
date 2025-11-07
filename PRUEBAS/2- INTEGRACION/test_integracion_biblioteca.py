import requests
import unittest
from bs4 import BeautifulSoup
import random
import unicodedata


BASE = "https://biblioteca-cubo.com/Biblioteca-CUBO/public"
REGISTER_URL = f"{BASE}/user/registerUser"
LOGIN_URL = f"{BASE}/user/loginUser"
PERFIL_URL = f"{BASE}/perfil"
LEER_URL = f"{BASE}/libros/EP02025/leer"


class TestIntegracionBiblioteca(unittest.TestCase):
    """Pruebas de integración de los módulos principales de Biblioteca CUBO."""

    @classmethod
    def setUpClass(cls):
        cls.session = requests.Session()
        cls.user_email = f"integracion_{random.randint(1000,9999)}@example.com"
        cls.user_pass = "12345678"
        print("\n=== Iniciando pruebas de Integración del sistema Biblioteca CUBO ===\n")

    # --------------------------------------------------------------
    # Utilidad: obtener token CSRF
    # --------------------------------------------------------------
    def get_csrf(self, url):
        r = self.session.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        token_tag = soup.find("input", {"name": "_token"})
        return token_tag["value"] if token_tag else None

    # --------------------------------------------------------------
    # Normaliza texto (minúsculas + sin tildes)
    # --------------------------------------------------------------
    def limpiar_texto(self, texto):
        texto = texto.lower()
        texto = ''.join(c for c in unicodedata.normalize('NFD', texto)
                        if unicodedata.category(c) != 'Mn')
        return texto

    # --------------------------------------------------------------
    # Paso 1: Registro
    # --------------------------------------------------------------
    def test_1_registro(self):
        token = self.get_csrf(REGISTER_URL)
        payload = {
            "_token": token,
            "nombre": "Integracion Prueba",
            "edad": "24",
            "sexo": "Masculino",
            "correo": self.user_email,
            "username": f"userint{random.randint(100,999)}",
            "telefono": "70001111",
            "direccion": "San Miguel",
            "password": self.user_pass,
            "password_confirmation": self.user_pass
        }
        r = self.session.post(REGISTER_URL, data=payload, allow_redirects=True)
        texto = self.limpiar_texto(r.text)

        print("\n[Registro de usuario]")
        print("Status:", r.status_code)
        self.assertIn(r.status_code, [200, 302])
        self.assertTrue(
            any(k in texto for k in ["perfil", "bienvenido", "cerrar sesion", "biblioteca cubo"]),
            "El registro no redirigió o no mostró sesión activa."
        )

    # --------------------------------------------------------------
    # Paso 2: Login
    # --------------------------------------------------------------
    def test_2_login(self):
        token = self.get_csrf(LOGIN_URL)
        payload = {
            "_token": token,
            "email": self.user_email,
            "password": self.user_pass
        }
        r = self.session.post(LOGIN_URL, data=payload, allow_redirects=True)
        texto = self.limpiar_texto(r.text)

        print("\n[Inicio de sesión]")
        print("Status:", r.status_code)
        self.assertIn(r.status_code, [200, 302])
        self.assertTrue(
            any(k in texto for k in ["perfil", "cerrar sesion", "inicio", "bienvenido"]),
            "No se detectó login exitoso."
        )

    # --------------------------------------------------------------
    # Paso 3: Perfil (validación tolerante + lectura de botones)
    # --------------------------------------------------------------
    def test_3_perfil(self):
        r = self.session.get(PERFIL_URL)
        soup = BeautifulSoup(r.text, "html.parser")

        texto_completo = soup.get_text(" ", strip=True).lower()
        texto_completo = ''.join(c for c in unicodedata.normalize('NFD', texto_completo)
                                 if unicodedata.category(c) != 'Mn')

        valores_inputs = [i.get('placeholder', '') for i in soup.find_all('input')]
        valores_inputs += [i.get('value', '') for i in soup.find_all('input')]
        valores_inputs += [b.get_text(strip=True) for b in soup.find_all('button')]
        texto_extra = ' '.join(valores_inputs).lower()
        texto_extra = ''.join(c for c in unicodedata.normalize('NFD', texto_extra)
                              if unicodedata.category(c) != 'Mn')

        texto = texto_completo + " " + texto_extra

        print("\n[Acceso al perfil]")
        print("Status:", r.status_code)

        palabras_clave = [
            "nombre", "nombre completo", "usuario", "correo", "correo electronico",
            "telefono", "direccion", "guardar cambios", "guardar", "actualizar",
            "informacion", "seguridad", "imagen"
        ]
        encontrados = [k for k in palabras_clave if k in texto]
        print("Palabras detectadas:", encontrados)

        self.assertEqual(r.status_code, 200)
        self.assertTrue(
            len(encontrados) >= 2,
            "El perfil cargó pero no se detectaron suficientes elementos del formulario."
        )

    # --------------------------------------------------------------
    # Paso 4: Lector de libros
    # --------------------------------------------------------------
    def test_4_leer_libro(self):
        r = self.session.get(LEER_URL)
        texto = self.limpiar_texto(r.text)

        print("\n[Lector de libro]")
        print("Status:", r.status_code)

        claves_libro = [
            "el principito", "capitulo", "pagina siguiente",
            "pagina anterior", "indice", "modo noche", "lector"
        ]
        self.assertEqual(r.status_code, 200)
        self.assertTrue(
            any(k in texto for k in claves_libro),
            "El contenido del libro no se cargó correctamente."
        )

    # --------------------------------------------------------------
    # Paso 5: Flujo completo
    # --------------------------------------------------------------
    def test_5_flujo_completo(self):
        print("\n[Validación del flujo completo]")
        self.test_1_registro()
        self.test_2_login()
        self.test_3_perfil()
        self.test_4_leer_libro()
        print("Flujo integral ejecutado correctamente.")

    @classmethod
    def tearDownClass(cls):
        print("\n=== Fin de pruebas de Integración del sistema Biblioteca CUBO ===\n")


if __name__ == "__main__":
    unittest.main()