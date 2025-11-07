import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class TestUsabilidadBiblioteca(unittest.TestCase):
    """Prueba de usabilidad del sistema Biblioteca CUBO (Cuadrante 3 – Usabilidad)."""

    @classmethod
    def setUpClass(cls):
        # Configuración del navegador (modo headless)
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

        cls.driver = webdriver.Chrome(options=options)
        cls.driver.implicitly_wait(10)
        cls.base = "https://biblioteca-cubo.com/Biblioteca-CUBO/public"

        print("\n=== Iniciando pruebas de Usabilidad del sistema Biblioteca CUBO ===\n")

    # ---------------------------------------------------------------
    # Utilidad: medir tiempo de carga
    # ---------------------------------------------------------------
    def medir_tiempo_carga(self, url):
        inicio = time.time()
        self.driver.get(url)
        fin = time.time()
        return round(fin - inicio, 2)

    # ---------------------------------------------------------------
    # Caso 1 – Usabilidad de la página de registro
    # ---------------------------------------------------------------
    def test_1_usabilidad_registro(self):
        url = f"{self.base}/user/registerUser"
        tiempo = self.medir_tiempo_carga(url)
        print(f"\n[Usabilidad – Registro]\nTiempo de carga: {tiempo}s")

        campos = ["nombre", "edad", "sexo", "correo", "username", "telefono", "direccion", "password"]
        for campo in campos:
            elementos = self.driver.find_elements(By.NAME, campo)
            self.assertTrue(elementos, f"No se encontró el campo '{campo}' en Registro.")

        boton = self.driver.find_elements(By.XPATH, "//button[contains(.,'Registrarse')]")
        self.assertTrue(boton, "No se encontró el botón 'Registrarse'.")
        self.assertLessEqual(tiempo, 5.0, "La página de registro tarda demasiado en cargar.")

    # ---------------------------------------------------------------
    # Caso 2 – Usabilidad de la página de login (con advertencia)
    # ---------------------------------------------------------------
    def test_2_usabilidad_login(self):
        url = f"{self.base}/user/loginUser"
        tiempo = self.medir_tiempo_carga(url)
        print(f"\n[Usabilidad – Login]\nTiempo de carga: {tiempo}s")

        email_field = self.driver.find_elements(By.NAME, "email")
        pass_field = self.driver.find_elements(By.NAME, "password")
        boton_login = self.driver.find_elements(By.CLASS_NAME, "login-btn")

        self.assertTrue(email_field, "Falta campo 'email'.")
        self.assertTrue(pass_field, "Falta campo 'password'.")
        self.assertTrue(boton_login, "No se encontró botón 'Iniciar sesión'.")

        if tiempo > 5.0:
            print(f"Advertencia: el login tardó {tiempo}s (>5s, fuera del rango óptimo).")
        else:
            print(f"Tiempo de carga aceptable ({tiempo}s).")

    # ---------------------------------------------------------------
    # Caso 3 – Usabilidad del perfil de usuario (requiere login previo)
    # ---------------------------------------------------------------
    def test_3_usabilidad_perfil(self):
        self.driver.get(f"{self.base}/user/loginUser")

        self.driver.find_element(By.NAME, "email").send_keys("mp20049@ues.edu.sv")
        self.driver.find_element(By.NAME, "password").send_keys("12345678")
        self.driver.find_element(By.CLASS_NAME, "login-btn").click()

        inicio = time.time()
        self.driver.get(f"{self.base}/perfil")
        fin = time.time()
        tiempo = round(fin - inicio, 2)

        print(f"\n[Usabilidad – Perfil]\nTiempo de carga: {tiempo}s")

        page_text = self.driver.page_source.lower()
        elementos_visibles = [
            "guardar cambios", "información", "seguridad", "imagen",
            "nombre", "correo", "teléfono", "dirección"
        ]

        encontrados = [txt for txt in elementos_visibles if txt in page_text]
        print("Elementos detectados:", encontrados)

        self.assertIn(
            self.driver.title.lower(),
            ["biblioteca cubo", "mi perfil"],
            f"Título inesperado: {self.driver.title}"
        )

        self.assertLessEqual(tiempo, 5.0, "El perfil tardó demasiado en cargar.")
        self.assertTrue(len(encontrados) >= 3, "El perfil cargó pero no se detectaron suficientes elementos.")

    # ---------------------------------------------------------------
    # Caso 4 – Usabilidad del lector de libros digitales (al final)
    # ---------------------------------------------------------------
    def test_4_usabilidad_leer(self):
        url = f"{self.base}/libros/EP02025/leer"
        inicio = time.time()
        self.driver.get(url)
        fin = time.time()
        tiempo = round(fin - inicio, 2)

        print(f"\n[Usabilidad – Lector de Libros]\nTiempo de carga: {tiempo}s")

        page_text = self.driver.page_source.lower()
        botones = ["página siguiente", "página anterior", "índice", "modo noche", "justificar"]
        encontrados = [b for b in botones if b in page_text]
        print("Botones detectados:", encontrados)

        self.assertTrue(
            any(k in page_text for k in ["el principito", "capítulo", "lector"]),
            "El contenido del libro no se cargó correctamente."
        )

        self.assertLessEqual(tiempo, 5.0, "El lector tardó demasiado en cargar.")
        self.assertTrue(len(encontrados) >= 2, "No se detectaron los controles principales de lectura.")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        print("\n=== Fin de pruebas de Usabilidad del sistema Biblioteca CUBO ===\n")


if __name__ == "__main__":
    unittest.main()