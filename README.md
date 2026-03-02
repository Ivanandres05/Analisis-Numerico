# Análisis Numérico - Métodos Aplicados a Software

Esta es una aplicación interactiva desarrollada en Python con una interfaz gráfica (GUI) que implementa herramientas de análisis numérico para encontrar raíces de ecuaciones algebraicas y trascendentes. Cada método ha sido enfocado en resolver problemas aplicados a la Ingeniería de Software (balanceo de servidores, tiempos de ejecución, base de datos, etc.).

## ��� Características
* **Interfaz Gráfica Intuitiva**: Construida con `tkinter` y `ttk`, permite navegar de manera fluida entre cada uno de los métodos sin reiniciar el programa.
* **Visualización Dinámica**: Gráficas en tiempo real totalmente integradas utilizando `matplotlib` (curvas de convergencia, funciones cruzando el eje X, gráficas de telaraña en Punto Fijo).
* **Robustez y Seguridad**: Manejo estricto de errores para evitar que el programa falle (cero en divisiones, intervalos sin cambio de signo, divergencia matemática y entradas alfanuméricas inválidas).
* **Suite de Pruebas**: Pruebas unitarias automáticas que validan los casos límite empleando `unittest`.

## ��� Métodos Implementados
1. **Bisección**: Aplicado al rendimiento y cuellos de botella en bases de datos.
2. **Falsa Posición**: Aplicado a la latencia en redes y procesos dependientes de transferencia de datos.
3. **Punto Fijo**: Aplicado a modelos de carga computacional y prevención de cuellos de botella en servidores.
4. **Newton-Raphson**: Aplicado al modelo de tiempo de ejecución de procesamiento por hilos de CPU (Threads).
5. **Secante**: Aplicado a las proyecciones y estimaciones de crecimiento de la base de usuarios.

## ��� Estructura del Proyecto
```text
Analisis Numerico/
├── funciones/         # Definiciones (lambdas/funciones core) de los problemas matemáticos.
├── interfaz/          # Componentes de la interfaz de usuario (ventanas, paneles, campos y figuras).
├── metodos/           # Lógica pura de los algoritmos (bisección, falsa posición, etc.).
├── tests/             # Scripts de validación y testeo unitario (TDD/Unit Testing).
├── utils/             # Funciones de filtrado de datos (validaciones.py) para el escudo de errores.
├── main.py            # Archivo maestro de arranque de la aplicación.
└── requirements.txt   # Lista de dependencias y paquetes de Python necesarios.
```

## ��� Instalación y Requisitos
* **Python 3.8 o superior**.
* Uso recomendado con Entornos Virtuales (`venv`).

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/Ivanandres05/Analisis-Numerico.git
   cd Analisis-Numerico
   ```

2. **Crear y activar el entorno virtual:**
   ```bash
   # En Windows:
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Instalar las dependencias del proyecto:**
   ```bash
   pip install -r requirements.txt
   ```
   *(Dependencias principales: `numpy` y `matplotlib`)*

## ��� Ejecución de la Aplicación
Para arrancar el entorno gráfico de la práctica solo ejecuta el siguiente comando estando en la raíz del proyecto:
```bash
python main.py
```

## ✅ Ejecución de Pruebas Unitarias
Para correr los tests en todos los módulos y comprobar que los límites matemáticos se evalúan con precisión:
```bash
python -m unittest discover tests
```
