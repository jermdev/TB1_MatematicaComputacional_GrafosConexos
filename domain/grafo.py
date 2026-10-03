from .vertice import Vertice
from .arista import Arista

class Grafo:
    def __init__(self, dirigido: bool = False):
        self.dirigido = dirigido
        self._vertices: dict[str, Vertice] = {}
        self._aristas: list[Arista] = []
        self._adyacencia: dict[str, list[str]] = {}

    def agregar_vertice(self, vertice: Vertice) -> None:
        v_id = str(vertice.id)
        if v_id in self._vertices:
            raise ValueError(f"Vértice {v_id} ya existe")
        self._vertices[v_id] = vertice
        self._adyacencia[v_id] = []

    def agregar_arista(self, arista: Arista) -> None:
        origen = str(arista.origen)
        destino = str(arista.destino)
        if origen not in self._vertices or destino not in self._vertices:
            raise ValueError(f"Ambos vértices ({origen}, {destino}) deben existir antes de conectar")
        self._aristas.append(arista)
        self._adyacencia[origen].append(destino)
        if not (arista.dirigida or self.dirigido):
            if origen != destino:
                self._adyacencia[destino].append(origen)

    @property
    def vertices(self) -> list[Vertice]:
        return list(self._vertices.values())

    @property
    def aristas(self) -> list[Arista]:
        return list(self._aristas)

    def vecinos(self, vertice_id: str) -> list[str]:
        return self._adyacencia.get(str(vertice_id), [])

    def get_lista_adyacencia(self) -> dict[str, list[str]]:
        return self._adyacencia

    def get_matriz(self) -> list[list[int]]:
        vertices = self.vertices
        ids = [vertice.id for vertice in vertices]
        posiciones = {vertice_id: indice for indice, vertice_id in enumerate(ids)}

        matriz = [
            [0 for _ in ids]
            for _ in ids
        ]

        for arista in self.aristas:
            origen = posiciones.get(str(arista.origen))
            destino = posiciones.get(str(arista.destino))

            if origen is not None and destino is not None:
                matriz[origen][destino] = 1

                if not (arista.dirigida or self.dirigido):
                    matriz[destino][origen] = 1

        return matriz