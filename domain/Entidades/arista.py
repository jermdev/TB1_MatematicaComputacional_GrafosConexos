
from typing import Any

class Arista:
    def __init__(self, origen: str, destion: str = None, peso: float = 1.00, dirigida: bool = False, destino: str = None):
        self._origen = str(origen)
        self._destino = str(destino if destino is not None else destion)
        self._peso = peso
        self._dirigida = dirigida
        self._atributos: dict[str, Any] = {}

    @property
    def origen(self):
        return self._origen
    
    @property
    def destino(self):
        return self._destino
    
    @property
    def peso(self):
        return self._peso

    @property
    def dirigida(self):
        return self._dirigida

    def get_atributo(self, key: str) -> Any:
        return self._atributos.get(key, None)
    
    def set_atributo(self, key: str, value: Any):
        self._atributos[key] = value
        