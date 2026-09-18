
from domain.vertice import Vertice
from domain.grafo import Grafo
from algorithms.algoritmo_conectividad_grafo import AlgoritmoConectividadGrafo
class grafoService:
    def __init__(self, grafoRepository: Grafo = None, algoritmo_conectividad_grafo: AlgoritmoConectividadGrafo = None):
        self.grafoRepository = grafoRepository
        self.algoritmo_conectividad_grafo = algoritmo_conectividad_grafo



    def push_vertice(self, vertice: Vertice):
        return self.grafoRepository.agregar_vertice(vertice)

    def push_arista(self, vertice1: Vertice, vertice2: Vertice):
        return self.grafoRepository.agregar_arista(vertice1, vertice2)

    def get_vertice(self, vertice: Vertice):
        return self.grafoRepository.get_vertice(vertice)

    def get_aristas(self, vertice: Vertice):
        return self.grafoRepository.get_aristas(vertice)

    def get_lista_adyacencia(self):
        return self.grafoRepository.get_lista_adyacencia()

    def get_matriz(self):
        return self.grafoRepository.get_matriz()

    def get_algoritmo_conectividad_grafo(self):
        return self.algoritmo_conectividad_grafo