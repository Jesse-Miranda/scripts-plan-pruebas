import requests  # Importa la librería para hacer solicitudes HTTP.
import unittest  # Importa la librería para realizar pruebas unitarias.
from bs4 import BeautifulSoup  # Importa BeautifulSoup para parsear y manipular HTML.
import random  # Importa la librería random para generar datos aleatorios en las pruebas.
import unicodedata  # Importa unicodedata para normalizar y eliminar tildes.

# URLs base para el registro, login, perfil y lectura de libros
BASE = "https://biblioteca-cubo.com/Biblioteca-CUBO/public"
REGISTER_URL = f"{BASE}/user/registerUser"
LOGIN_URL = f"{BASE}/user/loginUser"
PERFIL_URL = f"{BASE}/perfil"
LEER_URL = f"{BASE}/libros/EP02025/leer"

class TestIntegracionBiblioteca(unittest.TestCase):
    # Pruebas de integración de los módulos principales de Biblioteca CUBO.

    @classmethod
    def setUpClass(cls):
        # Configuración inicial que se ejecuta una vez antes de todas las pruebas.
        cls.session = requests.Session()  # Crea una nueva sesión para mantener las cookies entre solicitudes.
        cls.user_email = f"integracion_{random.randint(1000,9999)}@example.com"  # Email del usuario de prueba.
        cls.user_pass = "12345678"  # Contraseña del usuario de prueba.
        print("\n=== INICIANDO PRUEBAS DE INTEGRACION DE SISTEMA WEB BIBLIOTECA VIRTUAL CUBO ===\n")

    # --------------------------------------------------------------
    # Utilidad: obtener token CSRF
    # --------------------------------------------------------------
    def get_csrf(self, url):
        # Obtiene el token CSRF de la página para prevenir ataques CSRF.
        r = self.session.get(url)  # Realiza una solicitud GET a la URL proporcionada.
        soup = BeautifulSoup(r.text, "html.parser")  # Analiza el HTML de la respuesta.
        token_tag = soup.find("input", {"name": "_token"})  # Busca el campo del token CSRF.
        return token_tag["value"] if token_tag else None  # Retorna el token si lo encuentra.

    # --------------------------------------------------------------
    # Normaliza texto (minúsculas + sin tildes)
    # --------------------------------------------------------------
    def limpiar_texto(self, texto):
        # Normaliza el texto a minúsculas y elimina las tildes.
        texto = texto.lower()
        texto = ''.join(c for c in unicodedata.normalize('NFD', texto)
                        if unicodedata.category(c) != 'Mn')  # Elimina las marcas de acento (tildes).
        return texto

    # --------------------------------------------------------------
    # Paso 1: Registro
    # --------------------------------------------------------------
    def test_1_registro(self):
        # Verifica que el registro de usuario funcione correctamente.
        token = self.get_csrf(REGISTER_URL)  # Obtiene el token CSRF.
        payload = {
            "_token": token,
            "nombre": "Integracion Prueba",  # Nombre del usuario.
            "edad": "24",  # Edad del usuario.
            "sexo": "Masculino",  # Sexo del usuario.
            "correo": self.user_email,  # Correo electrónico del usuario.
            "username": f"userint{random.randint(100,999)}",  # Nombre de usuario único.
            "telefono": "70001111",  # Teléfono del usuario.
            "direccion": "San Miguel",  # Dirección del usuario.
            "password": self.user_pass,  # Contraseña del usuario.
            "password_confirmation": self.user_pass  # Confirmación de contraseña.
        }
        r = self.session.post(REGISTER_URL, data=payload, allow_redirects=True)  # Envía los datos del formulario.
        texto = self.limpiar_texto(r.text)  # Normaliza el texto de la respuesta.

        print("\n[Registro de usuario]")
        print("Status:", r.status_code)

        # Verifica que la respuesta sea 200 (OK) o 302 (Redirección).
        self.assertIn(r.status_code, [200, 302])
        # Verifica que la respuesta contenga palabras clave relacionadas con el inicio de sesión.
        self.assertTrue(
            any(k in texto for k in ["perfil", "bienvenido", "cerrar sesion", "biblioteca cubo"]),
            "El registro no redirigió o no mostró sesión activa."
        )

    # --------------------------------------------------------------
    # Paso 2: Login
    # --------------------------------------------------------------
    def test_2_login(self):
        # Verifica que el login de usuario funcione correctamente.
        token = self.get_csrf(LOGIN_URL)  # Obtiene el token CSRF para el login.
        payload = {
            "_token": token,
            "email": self.user_email,  # Email del usuario.
            "password": self.user_pass  # Contraseña del usuario.
        }
        r = self.session.post(LOGIN_URL, data=payload, allow_redirects=True)  # Envía los datos del formulario.
        texto = self.limpiar_texto(r.text)  # Normaliza el texto de la respuesta.

        print("\n[Inicio de sesión]")
        print("Status:", r.status_code)

        # Verifica que la respuesta sea 200 (OK) o 302 (Redirección).
        self.assertIn(r.status_code, [200, 302])
        # Verifica que la respuesta contenga palabras clave relacionadas con el inicio de sesión.
        self.assertTrue(
            any(k in texto for k in ["perfil", "cerrar sesion", "inicio", "bienvenido"]),
            "No se detectó login exitoso."
        )

    # --------------------------------------------------------------
    # Paso 3: Perfil (validación tolerante + lectura de botones)
    # --------------------------------------------------------------
    def test_3_perfil(self):
        # Verifica que la página de perfil cargue correctamente.
        r = self.session.get(PERFIL_URL)  # Realiza una solicitud GET a la página del perfil.
        soup = BeautifulSoup(r.text, "html.parser")  # Analiza el HTML de la página.

        # Obtiene el texto completo de la página y lo normaliza.
        texto_completo = soup.get_text(" ", strip=True).lower()
        texto_completo = ''.join(c for c in unicodedata.normalize('NFD', texto_completo)
                                 if unicodedata.category(c) != 'Mn')

        # Obtiene los valores de los inputs y botones.
        valores_inputs = [i.get('placeholder', '') for i in soup.find_all('input')]
        valores_inputs += [i.get('value', '') for i in soup.find_all('input')]
        valores_inputs += [b.get_text(strip=True) for b in soup.find_all('button')]
        texto_extra = ' '.join(valores_inputs).lower()
        texto_extra = ''.join(c for c in unicodedata.normalize('NFD', texto_extra)
                              if unicodedata.category(c) != 'Mn')

        texto = texto_completo + " " + texto_extra  # Junta el texto completo.

        print("\n[Acceso al perfil]")
        print("Status:", r.status_code)

        # Palabras clave que deberían estar presentes en el perfil.
        palabras_clave = [
            "nombre", "nombre completo", "usuario", "correo", "correo electronico",
            "telefono", "direccion", "guardar cambios", "guardar", "actualizar",
            "informacion", "seguridad", "imagen"
        ]
        encontrados = [k for k in palabras_clave if k in texto]  # Busca las palabras clave en el texto.
        print("Palabras detectadas:", encontrados)

        # Verifica que la respuesta sea 200 (OK).
        self.assertEqual(r.status_code, 200)
        # Verifica que se detectaron al menos 2 palabras clave en el perfil.
        self.assertTrue(
            len(encontrados) >= 2,
            "El perfil cargó pero no se detectaron suficientes elementos del formulario."
        )

    # --------------------------------------------------------------
    # Paso 4: Lector de libros
    # --------------------------------------------------------------
    def test_4_leer_libro(self):
        # Verifica que el lector de libros cargue correctamente.
        r = self.session.get(LEER_URL)  # Realiza una solicitud GET a la página de lectura del libro.
        texto = self.limpiar_texto(r.text)  # Normaliza el texto de la respuesta.

        print("\n[Lector de libro]")
        print("Status:", r.status_code)

        # Palabras clave que deberían estar presentes en el contenido del libro.
        claves_libro = [
            "el principito", "capitulo", "pagina siguiente",
            "pagina anterior", "indice", "modo noche", "lector"
        ]
        # Verifica que el contenido del libro se haya cargado correctamente.
        self.assertEqual(r.status_code, 200)
        self.assertTrue(
            any(k in texto for k in claves_libro),
            "El contenido del libro no se cargó correctamente."
        )

    # --------------------------------------------------------------
    # Paso 5: Flujo completo
    # --------------------------------------------------------------
    def test_5_flujo_completo(self):
        # Verifica que el flujo completo (registro, login, perfil, lectura) funcione correctamente.
        print("\n[Validación del flujo completo]")
        self.test_1_registro()  # Ejecuta el paso de registro.
        self.test_2_login()  # Ejecuta el paso de login.
        self.test_3_perfil()  # Ejecuta el paso de validación de perfil.
        self.test_4_leer_libro()  # Ejecuta el paso de validación del lector de libros.
        print("Flujo integral ejecutado correctamente.")

    @classmethod
    def tearDownClass(cls):
        # Método de limpieza que se ejecuta una vez después de todas las pruebas.
        print("\n\n=== PRUEBAS DE INTEGRACION DE SISTEMA WEB BIBLIOTECA VIRTUAL CUBO FINALIZADAS ===\n")

# Ejecuta las pruebas cuando el script es ejecutado directamente.
if __name__ == "__main__":
    unittest.main()
