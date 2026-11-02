# Contexto del Proyecto

Este es un proyecto pequeño para la visualización y análisis de grafos y sus componentes conexas utilizando algoritmos de exploración (BFS, DFS). El objetivo de este documento es establecer las reglas de desarrollo, el flujo de trabajo y la arquitectura que los asistentes de IA deben respetar estrictamente.

## Stack Tecnológico

- **Lenguaje:** `python==3.14.6`
- **Librerías principales:**
  - `pandas==3.0.6`
  - `pyvis==0.3.2`
  - `streamlit==1.63.0`

---

## Estructura de Carpetas

El proyecto sigue una estructura modular simple. La IA debe respetar estrictamente esta jerarquía y no inventar directorios ni archivos fuera de esta lógica sin indicación explícita.

```text
/
├── damin/                                   # Core / Dominio de la aplicación (Entidades y Algoritmos)
│   ├── Entidades/                           # Modelos del dominio
│   │   ├── arista.py                        # Conexiones entre vértices
│   │   ├── grafo.py                         # Estructura principal (vértices y aristas)
│   │   ├── paso_algoritmo.py                # Estado/progreso de la ejecución del algoritmo
│   │   └── vertice.py                       # Nodo del grafo (id, etiqueta, metadata)
│   └── algorithms/                          # Lógica pura de algoritmos sobre el grafo
│       ├── algoritmo_conectividad_grafo.py  # Clase base para algoritmos de conectividad
│       ├── bfs.py                           # Algoritmo de exploración en anchura (BFS)
│       └── dfs.py                           # Algoritmo de exploración en profundidad (DFS)
├── service/                                 # Capa de servicios y orquestación
│   ├── generardor_grafo_service.py          # Generación e inicialización de grafos
│   ├── grafo_orquestador.py                 # Orquestador que coordina servicios y entidades
│   └── grafo_service.py                     # Operaciones y manipulación de la entidad Grafo
├── UI/                                      # Capa de presentación (Streamlit)
│   ├── components/
│   │   ├── controles.py                     # Widgets y controles de entrada del usuario
│   │   ├── grafo_canva.py                   # Renderizado visual del grafo (PyVis)
│   │   └── progreso_pasos.py                # Componente para mostrar la ejecución paso a paso
│   └── index.py                             # Punto de entrada de la interfaz de usuario
├── main.py                                  # Punto de entrada de la aplicación
└── CONTEXT.md                               # Este archivo de contexto y reglas
```

 ## Comunicación Unidireccional Estricta
UI únicamente consume componentes de service. No interactúa directamente con la lógica interna de los algoritmos ni manipula las entidades sin pasar por la capa de servicio.

service coordina los procesos, orquesta el estado y consume el dominio damin (Entidades y Algoritmos).

damin es el Core puro: no tiene ninguna dependencia hacia service ni hacia UI. Solo seria necesarioquisiera  como tipo de dato, para
algun metodo o funcion, pero no se instancia ninguna clase de core en la  capa de UI.

## Sin Contratos ni Interfaces

NO implementar clases abstractas de interfaz (ABCs) ni contratos explícitos para desacoplar capas. Dado el tamaño del proyecto, no son necesarios y añaden complejidad innecesaria.

La separación de responsabilidades se garantiza mediante la división modular de carpetas y la disciplina en las importaciones.

## Reglas de Desarrollo para Agentes de IA

Respeto a la Estructura: No modifiques ni crees nuevas carpetas principales (damin, service, UI) sin autorización.

División de Responsabilidades:

La capa UI no debe contener algoritmos de grafos ni lógica de negocio; solo lógica de renderizado en Streamlit.

Las entidades en damin/Entidades/ deben ser estructuras de datos puras o con comportamiento inherente a su modelo.

La lógica de ejecución paso a paso de los algoritmos pertenece exclusivamente a damin/algorithms/.

Manejo del Estado: La coordinación del estado de la aplicación (como el progreso de un algoritmo o la actualización del grafo activo) se gestiona en service/grafo_orquestador.py o service/grafo_service.py.

Python Idiomático y Tipado: Utiliza type hints nativos de Python (def ejecutar(self, grafo: Grafo) -> list[PasoAlgoritmo]:) para mantener el código claro sin necesidad de interfaces.

## Flujo de Trabajo para Nuevas Funcionalidades

Cuando se pida implementar un nuevo módulo o algoritmo, la IA debe seguir este orden de desarrollo:

Dominio (damin/): Crear/actualizar las entidades en damin/Entidades/ o el algoritmo en damin/algorithms/ derivando de algoritmo_conectividad_grafo.py.

Servicio (service/): Exponer la nueva funcionalidad en grafo_service.py o coordinarla en grafo_orquestador.py.

Interfaz (UI/): Crear el componente visual en UI/components/ y conectarlo en UI/index.py consumiendo los métodos del servicio.