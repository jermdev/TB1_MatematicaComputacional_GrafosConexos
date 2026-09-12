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