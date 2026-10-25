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

    def obtener_vertice(self, vertice_id: str) -> Vertice | None:
        return self._vertices.get(str(vertice_id))

    def obtener_etiqueta(self, vertice_id: str) -> str:
        v = self.obtener_vertice(vertice_id)
        return (v.etiqueta or str(v.id)) if v else str(vertice_id)

    def existe_arista(self, origen_id: str, destino_id: str) -> bool:
        u, v = str(origen_id), str(destino_id)
        for a in self._aristas:
            if a.origen == u and a.destino == v:
                return True
            if not (a.dirigida or self.dirigido) and a.origen == v and a.destino == u:
                return True
        return False

    def agregar_arista(self, arista: Arista) -> None:
        if arista.origen not in self._vertices or arista.destino not in self._vertices:
            raise ValueError("Ambos vértices deben existir antes de conectar")
        if self.existe_arista(arista.origen, arista.destino):
            return
        self._aristas.append(arista)
        self._adyacencia[arista.origen].append(arista.destino)
        if not (arista.dirigida or self.dirigido):
            self._adyacencia[arista.destino].append(arista.origen)

    @property
    def vertices(self) -> list[Vertice]:
        return list(self._vertices.values())

    @property
    def aristas(self) -> list[Arista]:
        return list(self._aristas)

    def vecinos(self, vertice_id: str) -> list[str]:
        return self._adyacencia.get(vertice_id, [])

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
            origen = posiciones[arista.origen]
            destino = posiciones[arista.destino]

            matriz[origen][destino] = 1

            if not (arista.dirigida or self.dirigido):
                matriz[destino][origen] = 1

        return matriz