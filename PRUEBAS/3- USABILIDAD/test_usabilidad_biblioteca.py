import unittest  # Importa la librería para realizar pruebas unitarias.
import time  # Importa la librería para medir el tiempo de ejecución.
from selenium import webdriver  # Importa Selenium para controlar el navegador.
from selenium.webdriver.common.by import By  # Importa la clase para buscar elementos por su localización.
from selenium.webdriver.chrome.options import Options  # Importa las opciones para configurar el navegador.

class TestUsabilidadBiblioteca(unittest.TestCase):
    # Prueba de usabilidad del sistema Biblioteca CUBO (Cuadrante 3 – Usabilidad).

    @classmethod
    def setUpClass(cls):
        # Configuración del navegador (modo headless).
        options = Options()
        options.add_argument("--headless=new")  # Ejecuta el navegador sin interfaz gráfica.
        options.add_argument("--disable-gpu")  # Desactiva la aceleración de GPU (opcional).
        options.add_argument("--window-size=1920,1080")  # Establece el tamaño de la ventana del navegador.

        # Inicializa el controlador de Selenium con las opciones definidas.
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.implicitly_wait(10)  # Espera implícita de 10 segundos para encontrar los elementos.
        cls.base = "https://biblioteca-cubo.com/Biblioteca-CUBO/public"  # URL base del sistema.

        print("\n=== INICIANDO PRUEBAS DE USABILIDAD DE SISTEMA WEB BIBLIOTECA VIRTUAL CUBO ===\n")

    # ---------------------------------------------------------------
    # Utilidad: medir tiempo de carga
    # ---------------------------------------------------------------
    def medir_tiempo_carga(self, url):
        # Mide el tiempo de carga de una página.
        inicio = time.time()  # Marca el inicio del tiempo.
        self.driver.get(url)  # Carga la URL.
        fin = time.time()  # Marca el final del tiempo.
        return round(fin - inicio, 2)  # Retorna el tiempo de carga en segundos (redondeado a 2 decimales).

    # ---------------------------------------------------------------
    # Caso 1 – Usabilidad de la página de registro
    # ---------------------------------------------------------------
    def test_1_usabilidad_registro(self):
        # Verifica la usabilidad de la página de registro.
        url = f"{self.base}/user/registerUser"  # URL de la página de registro.
        tiempo = self.medir_tiempo_carga(url)  # Mide el tiempo de carga de la página.
        print(f"\n[Usabilidad – Registro]\nTiempo de carga: {tiempo}s")

        # Lista de campos que deben aparecer en la página de registro.
        campos = ["nombre", "edad", "sexo", "correo", "username", "telefono", "direccion", "password"]
        # Verifica que cada campo esté presente en la página.
        for campo in campos:
            elementos = self.driver.find_elements(By.NAME, campo)
            self.assertTrue(elementos, f"No se encontró el campo '{campo}' en Registro.")

        # Verifica que el botón de registro esté presente.
        boton = self.driver.find_elements(By.XPATH, "//button[contains(.,'Registrarse')]")
        self.assertTrue(boton, "No se encontró el botón 'Registrarse'.")
        
        # Verifica que la página cargue en un tiempo razonable (menos de 5 segundos).
        self.assertLessEqual(tiempo, 5.0, "La página de registro tarda demasiado en cargar.")

    # ---------------------------------------------------------------
    # Caso 2 – Usabilidad de la página de login (con advertencia)
    # ---------------------------------------------------------------
    def test_2_usabilidad_login(self):
        # Verifica la usabilidad de la página de login.
        url = f"{self.base}/user/loginUser"  # URL de la página de login.
        tiempo = self.medir_tiempo_carga(url)  # Mide el tiempo de carga de la página.
        print(f"\n[Usabilidad – Login]\nTiempo de carga: {tiempo}s")

        # Verifica que los campos de email y password estén presentes.
        email_field = self.driver.find_elements(By.NAME, "email")
        pass_field = self.driver.find_elements(By.NAME, "password")
        boton_login = self.driver.find_elements(By.CLASS_NAME, "login-btn")

        self.assertTrue(email_field, "Falta campo 'email'.")
        self.assertTrue(pass_field, "Falta campo 'password'.")
        self.assertTrue(boton_login, "No se encontró botón 'Iniciar sesión'.")

        # Si el tiempo de carga es mayor a 5 segundos, se emite una advertencia.
        if tiempo > 5.0:
            print(f"Advertencia: el login tardó {tiempo}s (>5s, fuera del rango óptimo).")
        else:
            print(f"Tiempo de carga aceptable ({tiempo}s).")

    # ---------------------------------------------------------------
    # Caso 3 – Usabilidad del perfil de usuario (requiere login previo)
    # ---------------------------------------------------------------
    def test_3_usabilidad_perfil(self):
        # Inicia sesión con un usuario previamente registrado.
        self.driver.get(f"{self.base}/user/loginUser")
        self.driver.find_element(By.NAME, "email").send_keys("mp20049@ues.edu.sv")
        self.driver.find_element(By.NAME, "password").send_keys("12345678")
        self.driver.find_element(By.CLASS_NAME, "login-btn").click()

        # Mide el tiempo de carga de la página del perfil.
        inicio = time.time()
        self.driver.get(f"{self.base}/perfil")
        fin = time.time()
        tiempo = round(fin - inicio, 2)
        print(f"\n[Usabilidad – Perfil]\nTiempo de carga: {tiempo}s")

        # Obtiene el texto de la página y lo normaliza (sin tildes y en minúsculas).
        page_text = self.driver.page_source.lower()
        elementos_visibles = [
            "guardar cambios", "información", "seguridad", "imagen",
            "nombre", "correo", "teléfono", "dirección"
        ]

        encontrados = [txt for txt in elementos_visibles if txt in page_text]
        print("Elementos detectados:", encontrados)

        # Verifica que el título de la página sea el esperado.
        self.assertIn(
            self.driver.title.lower(),
            ["biblioteca cubo", "mi perfil"],
            f"Título inesperado: {self.driver.title}"
        )

        # Verifica que el tiempo de carga sea aceptable (menos de 5 segundos).
        self.assertLessEqual(tiempo, 5.0, "El perfil tardó demasiado en cargar.")
        
        # Verifica que al menos 3 elementos estén presentes en la página del perfil.
        self.assertTrue(len(encontrados) >= 3, "El perfil cargó pero no se detectaron suficientes elementos.")

    # ---------------------------------------------------------------
    # Caso 4 – Usabilidad del lector de libros digitales (al final)
    # ---------------------------------------------------------------
    def test_4_usabilidad_leer(self):
        # Verifica la usabilidad de la página del lector de libros.
        url = f"{self.base}/libros/EP02025/leer"  # URL del libro.
        inicio = time.time()
        self.driver.get(url)  # Carga la página del libro.
        fin = time.time()
        tiempo = round(fin - inicio, 2)
        print(f"\n[Usabilidad – Lector de Libros]\nTiempo de carga: {tiempo}s")

        # Obtiene el texto de la página y lo normaliza (sin tildes y en minúsculas).
        page_text = self.driver.page_source.lower()

        # Lista de botones que deben estar presentes en la página.
        botones = ["página siguiente", "página anterior", "índice", "modo noche", "justificar"]
        encontrados = [b for b in botones if b in page_text]
        print("Botones detectados:", encontrados)

        # Verifica que el contenido del libro cargue correctamente.
        self.assertTrue(
            any(k in page_text for k in ["el principito", "capítulo", "lector"]),
            "El contenido del libro no se cargó correctamente."
        )

        # Verifica que el tiempo de carga sea aceptable (menos de 5 segundos).
        self.assertLessEqual(tiempo, 5.0, "El lector tardó demasiado en cargar.")
        
        # Verifica que al menos 2 botones principales de navegación estén presentes.
        self.assertTrue(len(encontrados) >= 2, "No se detectaron los controles principales de lectura.")

    @classmethod
    def tearDownClass(cls):
        # Cierra el navegador al finalizar las pruebas.
        cls.driver.quit()
        print("\n=== PRUEBAS DE USABILIDAD DE SISTEMA WEB BIBLIOTECA VIRTUAL CUBO FINALIZADAS ===\n")

# Ejecuta las pruebas cuando el script es ejecutado directamente.
if __name__ == "__main__":
    unittest.main()
