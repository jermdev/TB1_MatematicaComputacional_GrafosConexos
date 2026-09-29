import random
from domain.arista import Arista
from domain.grafo import Grafo
from domain.vertice import Vertice


def _generar_etiqueta(indice: int) -> str:
    """Genera etiquetas A, B, C... Z, o V27, V28 si supera el abecedario."""
    if 1 <= indice <= 26:
        return chr(ord('A') + indice - 1)
    return f"V{indice}"


def crear_grafo_ejemplo() -> Grafo:
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


def generar_grafo_vacio(num_vertices: int, dirigido: bool = False) -> Grafo:
    """Crea un grafo con num_vertices vértices y sin aristas."""
    grafo = Grafo(dirigido=dirigido)
    for i in range(1, num_vertices + 1):
        v_id = str(i)
        etiqueta = _generar_etiqueta(i)
        grafo.agregar_vertice(Vertice(id=v_id, etiqueta=etiqueta))
    return grafo


def generar_grafo_aleatorio(num_vertices: int, probabilidad: float = 0.35, dirigido: bool = False) -> Grafo:
    """
    Genera un grafo con num_vertices vértices y aristas aleatorias
    según la probabilidad de conexión especificada.
    """
    grafo = generar_grafo_vacio(num_vertices, dirigido=dirigido)
    vertices_ids = [v.id for v in grafo.vertices]

    if num_vertices < 2:
        return grafo

    aristas_agregadas = 0
    if not dirigido:
        for i in range(len(vertices_ids)):
            for j in range(i + 1, len(vertices_ids)):
                if random.random() < probabilidad:
                    grafo.agregar_arista(Arista(vertices_ids[i], vertices_ids[j], peso=1.0, dirigida=False))
                    aristas_agregadas += 1

        # Si no se generó ninguna arista y hay al menos 2 vértices, conectamos 1 par al azar
        if aristas_agregadas == 0 and len(vertices_ids) >= 2:
            u, v = random.sample(vertices_ids, 2)
            grafo.agregar_arista(Arista(u, v, peso=1.0, dirigida=False))
    else:
        for u in vertices_ids:
            for v in vertices_ids:
                if u != v and random.random() < probabilidad:
                    grafo.agregar_arista(Arista(u, v, peso=1.0, dirigida=True))
                    aristas_agregadas += 1

    return grafo

