from domain.arista import Arista
from domain.grafo import Grafo
from domain.vertice import Vertice


def crear_grafo_ejemplo():
    grafo = Grafo()

    vertices = [
        Vertice("1", "A"),
        Vertice("2", "B"),
        Vertice("3", "C"),
        Vertice("4", "D"),
    ]

    for vertice in vertices:
        grafo.agregar_vertice(vertice)

    aristas = [
        Arista("1", "2"),
        Arista("2", "3"),
        Arista("3", "4"),
        Arista("4", "1"),
    ]

    for arista in aristas:
        grafo.agregar_arista(arista)

    return grafo


def parsear_conexiones(texto: str) -> list[tuple[str, str]]:
    """
    Parsea conexiones a partir de un texto libre.
    Formatos admitidos por línea o separados por punto y coma:
    - 1 2
    - 1, 2
    - 1-2
    - 1 -> 2
    """
    import re
    conexiones = []
    lineas = texto.replace(";", "\n").splitlines()
    for linea in lineas:
        linea = linea.strip()
        if not linea or linea.startswith("#"):
            continue
        tokens = re.findall(r'[^\s,\->]+', linea)
        if len(tokens) >= 2:
            conexiones.append((tokens[0], tokens[1]))
    return conexiones


def crear_grafo_manual(num_vertices: int, conexiones: list[tuple[str, str]], dirigido: bool = False) -> Grafo:
    grafo = Grafo(dirigido=dirigido)

    # 1. Crear vértices iniciales 1 .. num_vertices
    for i in range(1, num_vertices + 1):
        grafo.agregar_vertice(Vertice(str(i), str(i)))

    vertices_existentes = set(str(v.id) for v in grafo.vertices)

    # 2. Agregar conexiones
    for origen, destino in conexiones:
        orig_str = str(origen).strip()
        dest_str = str(destino).strip()

        # Si se hace referencia a un vértice que no fue inicializado, se agrega automáticamente
        if orig_str not in vertices_existentes:
            grafo.agregar_vertice(Vertice(orig_str, orig_str))
            vertices_existentes.add(orig_str)
        if dest_str not in vertices_existentes:
            grafo.agregar_vertice(Vertice(dest_str, dest_str))
            vertices_existentes.add(dest_str)

        grafo.agregar_arista(Arista(origen=orig_str, destino=dest_str, dirigida=dirigido))

    return grafo


def crear_grafo_desde_texto(num_vertices: int, texto_conexiones: str, dirigido: bool = False) -> Grafo:
    conexiones = parsear_conexiones(texto_conexiones)
    return crear_grafo_manual(num_vertices, conexiones, dirigido)


def generar_grafo_aleatorio(num_vertices: int, dirigido: bool = False, prob_conexion: float = 0.35) -> Grafo:
    import random
    grafo = Grafo(dirigido=dirigido)
    for i in range(1, num_vertices + 1):
        grafo.agregar_vertice(Vertice(str(i), str(i)))

    nodos = [str(i) for i in range(1, num_vertices + 1)]
    for i in range(len(nodos)):
        inicio_j = 0 if dirigido else (i + 1)
        for j in range(inicio_j, len(nodos)):
            if i != j and random.random() < prob_conexion:
                grafo.agregar_arista(Arista(origen=nodos[i], destino=nodos[j], dirigida=dirigido))

    return grafo
