# TB1 - Matemática Computacional: Simulador de Componentes Conexas de un Grafo

Aplicación web interactiva desarrollada con **Streamlit** y **Pyvis** para la visualización, exploración y análisis paso a paso de conectividad y componentes conexas en teoría de grafos mediante algoritmos como **DFS** (Búsqueda en Profundidad) y **BFS** (Búsqueda en Anchura).

---

## 🌟 Características Principales

- **Generación Flexible de Grafos:**
  - **Modo Automático:** Crea grafos aleatorios configurando el número de vértices (de 4 a 12) y ajustando la densidad de aristas (probabilidad de conexión).
  - **Modo Manual:** Crea un grafo con vértices etiquetados (`A`, `B`, `C`...) y permite conectar vértices manualmente, deshacer la última conexión o limpiar todas las aristas.
- **Visualización Interactiva con Pyvis (vis.js):**
  - Renderizado dinámico de nodos y aristas con física personalizable.
  - Manipulación directa en lienzo (zoom, paneo y arrastre de vértices).
  - **Persistencia de posiciones:** Conserva la disposición física de los nodos al avanzar o retroceder pasos en el algoritmo.
  - **Diferenciación cromática:** Resaltado de nodos visitados en tiempo real y coloreado por componentes conexas al finalizar el recorrido.
- **Representación Matricial:**
  - Alternancia entre la vista visual del grafo y su **Matriz de Adyacencia** estructurada con métricas clave ($|V|$, $|E|$ y tipo de grafo).
- **Ejecución Paso a Paso:**
  - Controles de navegación (**Anterior** / **Siguiente**) con bitácora explicativa detallada de cada paso (nodos visitados, estado de la cola/pila y vecinos analizados).

---

## 📋 Requisitos Previos

- **Python 3.10** o superior
- **Git**

---

## 🚀 Instalación y Puesta en Marcha

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/jermdev/TB1_MatematicaComputacional_GrafosConexos.git
   cd TB1_MatematicaComputacional_GrafosConexos
   ```

2. **Crear y activar el entorno virtual:**

   - **Windows (PowerShell):**
     ```powershell
     python -m venv venv
     venv\Scripts\activate
     ```

   - **Linux / macOS:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la aplicación:**
   ```bash
   python -m streamlit run main.py
   ```

   Una vez iniciada, Streamlit abrirá la aplicación automáticamente en tu navegador (por defecto en `http://localhost:8501`).

---

## 📁 Estructura del Proyecto

El proyecto está organizado siguiendo principios de modularidad, separando el dominio matemático, los algoritmos, la capa de servicios/orquestación y la interfaz de usuario:

```text
TB1_MatematicaComputacional_GrafosConexos/
├── main.py                             # Punto de entrada de la aplicación
├── requirements.txt                    # Dependencias del proyecto
├── .gitignore                          # Exclusiones de control de versiones
├── Readme.md                           # Documentación general del proyecto
│
├── domain/                             # Modelos del dominio (Teoría de Grafos)
│   ├── vertice.py                      # Clase Vertice (identificador, etiqueta, atributos)
│   ├── arista.py                       # Clase Arista (origen, destino, peso, dirección)
│   ├── grafo.py                        # Estructura de Grafo (gestión de adyacencia y matriz)
│   └── paso_algoritmo.py               # Modelo y tipos de pasos para la trazabilidad del algoritmo
│
├── algorithms/                         # Implementación de algoritmos de conectividad
│   ├── algoritmo_conectividad_grafo.py # Clase base abstracta para algoritmos de conectividad
│   ├── bfs.py                          # Algoritmo BFS (Breadth-First Search) paso a paso
│   └── dfs.py                          # Algoritmo DFS (Depth-First Search) paso a paso
│
├── service/                            # Lógica de negocio y orquestación
│   ├── grafo_orquestador.py            # Orquestador del estado global de la app y simulación
│   ├── generador_grafo_service.py      # Generación de grafos (ejemplo, vacío o aleatorio)
│   ├── grafo-service.py                # Servicio para operaciones sobre estructuras de grafo
│   └── conectividad_service.py         # Servicios complementarios de conectividad
│
├── UI/                                 # Capa de presentación (Streamlit)
│   ├── index.py                        # Layout principal en 3 columnas y control de eventos
│   └── components/                     # Componentes visuales modulares
│       ├── controles.py                # Panel de configuración, controles y navegación
│       ├── grafo_canva.py              # Canvas interactivo Pyvis y visor de matriz
│       └── progreso_pasos.py           # Panel visualizador del historial de pasos
│
└── utils/                              # Módulos auxiliares
    └── cargar_archivos.py              # Función para lectura de archivos relativa al proyecto
```

---

## 🔍 Detalle de Módulos y Componentes

### 1. `domain/`
- **[`vertice.py`](domain/vertice.py):** Modela cada nodo con su `id`, `etiqueta` descriptiva (p. ej., `A`, `B`, `C`) y diccionario de atributos genéricos.
- **[`arista.py`](domain/arista.py):** Modela la relación entre dos vértices, permitiendo configurar peso y dirección (dirigida / no dirigida).
- **[`grafo.py`](domain/grafo.py):** Mantiene la lista de vértices, aristas y listas de adyacencia. Contiene la lógica para validar conexiones y calcular la **matriz de adyacencia**.
- **[`paso_algoritmo.py`](domain/paso_algoritmo.py):** Define `Paso_Algoritmo` y la enumeración `Tipo_Paso` para capturar el estado exacto del algoritmo en cada iteración (nodo actual, cola/pila, visitados, mensaje descriptivo).

### 2. `algorithms/`
- **[`algoritmo_conectividad_grafo.py`](algorithms/algoritmo_conectividad_grafo.py):** Define el contrato abstracto mediante el método `es_conexo()`.
- **[`bfs.py`](algorithms/bfs.py):** Explora el grafo en anchura utilizando una cola (`collections.deque`), registrando cada paso para identificar componentes conexas y evaluar conectividad.
- **[`dfs.py`](algorithms/dfs.py):** Explora el grafo en profundidad utilizando una pila, registrando las decisiones de avance y agrupamiento de componentes conexas.

### 3. `service/`
- **[`grafo_orquestador.py`](service/grafo_orquestador.py):** Centro de coordinación del estado en la sesión de Streamlit. Controla la vista activa (`grafo` o `matriz`), el paso actual, la sincronización tras agregar o eliminar aristas y el recálculo automático de pasos.
- **[`generador_grafo_service.py`](service/generador_grafo_service.py):** Funciones para inicializar un grafo inicial de ejemplo, crear grafos vacíos con etiquetas automáticas (`A`-`Z`, `V27`...) o generar grafos aleatorios basados en probabilidad.
- **[`grafo-service.py`](service/grafo-service.py):** Capa de abstracción para interactuar con las operaciones de inserción y consulta del grafo.

### 4. `UI/`
- **[`index.py`](UI/index.py):** Configura la página en modo ancho (`wide`) y organiza la vista en tres columnas responsivas:
  1. *Izquierda:* Bitácora con la progresión del paso a paso.
  2. *Centro:* Lienzo interactivo del grafo con Pyvis o tabla de la matriz de adyacencia.
  3. *Derecha:* Panel de controles para parámetros, modos y botones de navegación.
- **[`UI/components/controles.py`](UI/components/controles.py):** Formularios interactivos para elegir número de vértices, densidad, tipo de algoritmo (DFS, BFS), agregar conexiones manuales y botones *Anterior* / *Siguiente*.
- **[`UI/components/grafo_canva.py`](UI/components/grafo_canva.py):** Integra la librería Pyvis mediante HTML embebido en Streamlit. Incluye scripts JavaScript para almacenar posiciones en `localStorage`/`sessionStorage` evitando que los nodos salten entre pasos.
- **[`UI/components/progreso_pasos.py`](UI/components/progreso_pasos.py):** Lista secuencialmente los pasos ejecutados resaltando el paso activo.

### 5. `utils/`
- **[`cargar_archivos.py`](utils/cargar_archivos.py):** Utilidad para resolver y leer rutas de archivos de manera independiente al sistema operativo.

---

## 🛠️ Tecnologías Utilizadas

- **[Python](https://www.python.org/)** (v3.10+)
- **[Streamlit](https://streamlit.io/)** - Framework para la creación de aplicaciones web interactivas en Python.
- **[Pyvis](https://pyvis.readthedocs.io/)** - Biblioteca basada en [vis.js](https://visjs.github.io/vis-network/docs/network/) para renderizado interactivo de grafos en red.
- **[Pandas](https://pandas.pydata.org/)** - Manipulación y visualización tabular de matrices de adyacencia.

---

## 📄 Licencia y Uso

Proyecto con fines académicos para la asignatura de **Matemática Computacional**.