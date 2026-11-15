<img width="736" height="310" alt="LogoUNAL" src="https://github.com/user-attachments/assets/73744e6f-1a2d-4a8e-88e1-b6811630c9cc" />

Actividad: Exercises Activity 4 - Manejo de Excepciones, Interfaces Gráficas y UML

Estudiante: Sebastian Vanegas Sanchez

Docente: Walter Hugo Arboleda Mazo 

# Taller Práctico 4: Manejo de Excepciones, Interfaces Gráficas (GUI) y Modelado UML en Python

Este repositorio reúne la solución de los ejercicios prácticos correspondientes al Taller 4, centrados en el control robusto de errores mediante excepciones nativas y personalizadas en Python, integrados con interfaces gráficas de escritorio desarrolladas en `tkinter` y `ttk`. Cada aplicación cuenta con su respectivo modelado arquitectónico en StarUML mediante **Diagramas de Clases** y **Diagramas de Casos de Uso**.

## Conceptos Aplicados
Durante el desarrollo de este taller se implementaron los siguientes conceptos técnicos y de diseño:
- **Separación de Responsabilidades (Backend / Frontend):** Desacoplamiento entre las clases de lógica de negocio/validación y las clases encargadas de la interfaz gráfica (`tkinter` y `ttk`).
- **Manejo de Excepciones Nativas y Bloques `try / except / finally`:** Captura controlada de `ZeroDivisionError`, `AttributeError`, `ValueError`, `IndexError`, `TypeError`, `ArithmeticError`, `FileNotFoundError`, `IsADirectoryError`, `PermissionError` y `UnicodeDecodeError`.
- **Jerarquías de Excepciones Personalizadas:** Definición y lanzamiento (`raise`) de excepciones específicas del dominio (`SimboloNuloError`, `SimboloInexistenteError`, `EquipoCompletoError`, `FormatoTextoInvalidoError`, `ContrasenaError`, `ErrorLecturaArchivo`).
- **Gestión de Rutas y Flujos de Bytes:** Resolución reproducible de rutas relativas con `pathlib.Path` y lectura binaria (`rb`) con decodificación UTF-8 línea por línea.
- **Modelado UML en StarUML:** Representación estructural mediante Diagramas de Clases (herencia, agregación, composición, dependencia y métodos estáticos) y funcional mediante Diagramas de Casos de Uso (`<<include>>` y `<<extend>>`).

## Estructura de los Ejercicios

### Ejercicio 6.4 (`ejercicio6.4.py`) - Simulador de Excepciones y Flujo `try-except-finally`
Aplicación orientada a demostrar el comportamiento del flujo de control frente a distintos fallos en tiempo de ejecución (`ZeroDivisionError`, `AttributeError` sobre referencias nulas, `ValueError` al convertir cadenas no numéricas e `IndexError` fuera de rango). La clase `Procesado` encapsula cada escenario garantizando el paso por el bloque `finally`, mientras que `GUI` permite ejecutar cada caso y visualizar tanto la traza en consola como la respuesta en pantalla.

### Ejercicio 6.5 (`ejercicio6.5.py`) - Gestión de Vendedores y Tabla ASCII
Sistema modular organizado en pestañas (`ttk.Notebook`) que integra dos módulos independientes:
- **Clase `Vendedor`:** Valida tipos de datos y restricciones de edad (rango válido y mayoría de edad) lanzando `TypeError` y `ValueError`.
- **Clase `TablaASCII`:** Utiliza un diccionario interno (`dict`) para almacenar y consultar códigos asociados a símbolos en $O(1)$, gestionando entradas vacías o claves inexistentes mediante las excepciones personalizadas `SimboloNuloError` y `SimboloInexistenteError`.

### Ejercicio 6.6 (`ejercicio6.6.py`) - Calculadora Numérica y Conversión de Bases
Aplicación matemática estructurada a partir de la clase utilitaria `CalculosNumericos`, cuyos métodos estáticos (`@staticmethod`) resuelven logaritmo neperiano, raíz cuadrada, pendiente de una recta, punto medio, raíces reales de ecuaciones cuadráticas y conversión de enteros decimales a cualquier base $b \in [2, 36]$. Incorpora validación estricta de dominio matemático (`ArithmeticError`, `ZeroDivisionError`, `ValueError`) y una consola integrada con soporte para copiar resultados al portapapeles.

### Ejercicio 6.7 (`ejercicio6.7.py`) - Equipos de Maratón de Programación y Validador de Contraseñas
Aplicación dividida en dos módulos funcionales con validación de reglas de negocio:
- **Equipos de Maratón (`Programador` y `EquipoMaratonProgramacion`):** Controla la creación de equipos de 2 a 3 integrantes y valida que los nombres y apellidos sean estrictamente alfabéticos y menores a 20 caracteres, lanzando `FormatoTextoInvalidoError` o `EquipoCompletoError` al alcanzar el cupo máximo.
- **Validador de Contraseñas (`Contrasena`):** Implementa una jerarquía de excepciones (`ContrasenaError`, `ContrasenasNoCoincidenError`, `RequisitosContrasenaError`) que verifica coincidencia, longitud mínima, ausencia de espacios y presencia de mayúsculas, minúsculas, dígitos y símbolos en un solo escaneo lineal.

### Ejercicio 6.8 (`ejercicio6.8.py`) - Lector de Archivos de Texto mediante Flujo de Bytes
Herramienta de lectura de archivos que desacopla la lógica de entrada/salida en la clase `LeerArchivo`. Resuelve rutas relativas respecto a la ubicación del script mediante `pathlib.Path`, abre el archivo como flujo de bytes (`rb`) y decodifica cada línea en UTF-8 para identificar con precisión el número de línea en caso de fallo de codificación (`ErrorLecturaArchivo`). La interfaz `AppLectorArchivoGUI` permite explorar archivos, visualizar el contenido original o en mayúsculas y copiarlo al portapapeles.

## 🛠️ Tecnologías y Herramientas
- **Lenguaje:** Python 3.x
- **Librerías Nativas:** `tkinter`, `ttk`, `math`, `pathlib`
- **Modelado de Software:** StarUML (Diagramas de Clases y Diagramas de Casos de Uso)