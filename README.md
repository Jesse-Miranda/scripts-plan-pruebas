# Scripts Plan de Pruebas
Este repositorio contiene los scripts desarrollados para la automatización del **Plan de Pruebas**, abarcando:
- Pruebas unitarias (registro, login, perfil)
- Pruebas de integración entre módulos
- Pruebas de usabilidad con Selenium
---
## Tecnologías
- Python 3.12  
- Selenium WebDriver  
- Requests + BeautifulSoup  
- Unittest Framework  
---
## Estructura del repositorio
Cada carpeta contiene pruebas enfocadas en un cuadrante del modelo **Agile Testing Quadrants**:
- **Cuadrante 1 (Unitarias):** Verifica las funciones críticas del sistema (registro, login, perfil).  
- **Cuadrante 2 (Integración):** Comprueba el flujo completo entre módulos del sistema.  
- **Cuadrante 3 (Usabilidad):** Evalúa tiempos de carga, accesibilidad y experiencia del usuario final.
---
## Ejecución de las pruebas
### Pruebas unitarias e integración
Ejecutar desde la terminal:
```bash
python -m unittest discover -s tests_unitarios
python -m unittest discover -s tests_integracion
python tests_usabilidad/test_usabilidad_biblioteca.py
```
---
## Autor

Jesse Antonio Miranda Pérez
Estudiante de Ingeniería de Sistemas Informáticos
Universidad de El Salvador – Facultad Multidisciplinaria Oriental
San Miguel, El Salvador
mp20049@ues.edu.sv
---
### **Add license**
Este proyecto está bajo la licencia MIT, lo que permite su uso con fines educativos y de investigación, otorgando el debido crédito al autor original.
---
