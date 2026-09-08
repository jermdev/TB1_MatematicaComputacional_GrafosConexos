from typing import Any

class Vertice:
    def __init__(self, id: str, etiqueta: str = ""):
        self._id = id
        self._etiqueta = etiqueta
        self._atributos = dict[str, Any] = {}

    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return isinstance(other, Vertice) and self.id == other.id

    @property
    def id(self):
        return self._id
    @property
    def etiqueta(self):
        return self._etiqueta

    def set_etiqueta(self, etiqueta: str):
        self._etiqueta = etiqueta

    def get_atributo(self, key: str) -> Any:
        return self._atributos.get(key, None)

    def set_atributo(self, key: str, value: Any):
        self._atributos[key] = value
    
