# Proyecto 1: Simulador interactivo de laberintos y rutas alternativas

**Asignatura:** Teoría de Grafos (INFO1158)  
**Integrantes:**
* Benjamín de la Fuente
* Jaime Levil
* Cristian Sáez

## Descripción
Aplicación interactiva desarrollada en Python para modelar un centro de almacenamiento mediante un grafo dirigido, permitiendo calcular el camino con menor número de pasillos (BFS), el máximo número de rutas independientes sin arcos compartidos (Edmonds-Karp con capacidad unitaria) y el corte mínimo de pasillos.

## Estructura del proyecto
* `algoritmos.py`: Implementación propia de la estructura `Grafo`, BFS, flujo máximo unitario, descomposición de caminos disjuntos, corte mínimo y verificaciones matemáticas.
* `datos.py`: Definición de los 11 vértices y 17 pasillos dirigidos de la red inicial.
* `app.py`: Interfaz gráfica interactiva desarrollada con `tkinter`.
* `verificacion.py`: Pruebas automatizadas y contraste con el caso manual de 5 vértices.

## Requisitos y dependencias
* **Python 3.8 o superior**.
* No requiere instalar bibliotecas externas. Utiliza únicamente módulos de la biblioteca estándar de Python (`tkinter`, `collections`, `math`).

## Instrucciones de ejecución
1. Clonar o descargar este repositorio.
2. Abrir una terminal en la carpeta del proyecto y ejecutar la interfaz gráfica:
   ```bash
   python app.py

