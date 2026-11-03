from domain.Entidades.arista import Arista
from domain.Entidades.vertice import Vertice
from domain.Entidades.grafo import Grafo
from domain.algorithms.algoritmo_conectividad_grafo import AlgoritmoConectividadGrafo


class grafoService:
    def __init__(self, dirigido: bool, grafoRepository: Grafo = None, algoritmo_conectividad_grafo: AlgoritmoConectividadGrafo = None):
        self.grafoRepository = grafoRepository if grafoRepository is not None else Grafo(dirigido=dirigido)
        self.algoritmo_conectividad_grafo = algoritmo_conectividad_grafo 

    def set_grafo(self, grafo: Grafo):
        self.grafoRepository = grafo

    def get_grafo(self) -> Grafo:
        return self.grafoRepository
    
    def push_vertice(self, vertice: Vertice):
        return self.grafoRepository.agregar_vertice(vertice)

    def push_arista(self, arista: Arista):
        return self.grafoRepository.agregar_arista(arista)

    def get_vertice(self, vertice_id: str):
        return self.grafoRepository.obtener_vertice(vertice_id)

    def get_vecinos(self, vertice_id: str):
        return self.grafoRepository.vecinos(vertice_id)

    def get_aristas(self):
        return self.grafoRepository.aristas

    def get_lista_adyacencia(self):
        return self.grafoRepository.get_lista_adyacencia()

    def get_matriz(self):
        return self.grafoRepository.get_matriz()

    def get_algoritmo_conectividad_grafo(self):
        return self.algoritmo_conectividad_grafo

    def set_algoritmo_conectividad_grafo(self, algoritmo: AlgoritmoConectividadGrafo):
        self.algoritmo_conectividad_grafo = algoritmo

    def ejecutar_algoritmo(self):
        if self.algoritmo_conectividad_grafo is not None:
            return self.algoritmo_conectividad_grafo.ejecutar(self.grafoRepository)
        return []

    def obtener_pasos(self) -> list:
        if self.algoritmo_conectividad_grafo is not None:
            return getattr(self.algoritmo_conectividad_grafo, "pasos", [])
        return []

    def obtener_componentes_conexas(self) -> list[list[str]]:
        if self.algoritmo_conectividad_grafo is not None:
            return getattr(self.algoritmo_conectividad_grafo, "componentes", [])
        return []

    def obtener_componentes_fuertemente_conexas(self) -> list[list[str]]:
        """Expone componentes fuertes solo para algoritmos que las implementen."""
        if self.algoritmo_conectividad_grafo is not None:
            obtener_componentes = getattr(
                self.algoritmo_conectividad_grafo,
                "encontrar_componentes_fuertemente_conexas",
                None,
            )
            if obtener_componentes is not None:
                return obtener_componentes(self.grafoRepository)
        return []

    def es_conexo(self, fuertemente: bool = False) -> bool:
        if self.algoritmo_conectividad_grafo is not None:
            # BFS conserva su contrato actual; esta opción solo se usa con algoritmos
            # que implementan explícitamente componentes fuertemente conexas.
            if fuertemente and hasattr(
                self.algoritmo_conectividad_grafo,
                "encontrar_componentes_fuertemente_conexas",
            ):
                return self.algoritmo_conectividad_grafo.es_conexo(
                    self.grafoRepository,
                    fuertemente=True,
                )
            return self.algoritmo_conectividad_grafo.es_conexo(self.grafoRepository)
        return False

    def obtener_etiqueta(self, vertice_id: str):
        return self.grafoRepository.obtener_etiqueta(vertice_id)

    def get_vertices(self):
        return self.grafoRepository.vertices

    def get_dirigido(self):
        return self.grafoRepository.dirigido
