from abc import ABC, abstractmethod

class AlgoritmoConectividadGrafo(ABC):

    def __init__(self, paso_a_paso: bool = False):
        self._paso_a_paso = paso_a_paso

    @abstractmethod
    def es_conexo(self, grafo):
        pass

    def set_paso_a_paso(self, paso_a_paso: bool):
        self._paso_a_paso = paso_a_paso

    @property
    def paso_a_paso(self) -> bool:
        return self._paso_a_paso
    

    