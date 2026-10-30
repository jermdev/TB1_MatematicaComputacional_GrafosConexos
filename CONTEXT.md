# Contexto del Proyecto

Este es un proyecto pequeño para [Describe exactamente qué hace la app, ej: un catálogo de películas sin anuncios]. El objetivo de este documento es establecer las reglas de desarrollo y la arquitectura para el asistente de IA.

## Stack Tecnológico
lenguaje: 
    python==3.14.6
librerias:
    pandas==3.0.6
    pyvis==0.3.2
    streamlit==1.63.0

## Estructura de Carpetas

El proyecto sigue una estructura modular simple. La IA debe respetar estrictamente esta jerarquía y no inventar directorios nuevos.

```text
/
├── damin/                                   # Aplicación cliente
│   ├── Entidades/                           # Entidades del Dominio de la aplicacion
│   │   ├── arista.py                        # Representa las conexione entre vertices
│   │   ├── grafo.py                         # Reune las estructuras de vertices y aristas
│   │   ├── paso_algoritmo.py                # Guarda el progeso del algortimo
│   │   ├── vertice.py                       # Representa un nodo del grafo, su id, etiqueta, e informacion adicional
│   ├── algorithms/                          # algortimos que se utilizaran para hallar las componentes conexas del grafo
│   │   ├── algoritmo_conectividad_grafo.py  # Clase Padre de las demas Clases que representan los algortimos para el grafo
│   │   ├── bfs.py                           # Algoritmo de exploracion por niveles.
│   │   └── dfs.py                           # Algortimo de eploracion profunda, primer algoritmo en ser implementado
├── service/                                 # Servicios que manipulan y gestionan el grafo y sus algoritmos
│   │   ├── generardor_grafo_service.py      # genera un grafo por defecto al inicizalizar el programa
│   │   ├── grafo_orquestador.py             # Gestiona el al servicio grafoService, este gestiona los servicios y entidades
│   │   ├── grafo_service.py                 # Gestiona la entidad grafo, representado a la entidad grafo atraves de su servicio 
├── UI/
│   ├── components/
│   │   ├── controles.py        # controles para manipular el grafo
│   │   ├── grafo_canva.py      # visualizacion del grafo
│   │   └── progreso_pasos.py   # progreso del algoritmo
│   ├── index.py             # interfaz de usuario del programa
└── CONTEXT.md          # Este archivo