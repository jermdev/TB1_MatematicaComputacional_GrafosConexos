from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional

class Tipo_Paso(Enum):
    INICIO = auto()
    VISITAR_NODO = auto()
    EXAMINAR_ARISTA = auto()
    ENCOLAR = auto()
    FIN = auto()

@dataclass
class Paso_Algoritmo:
    numero: int
    tipo: Tipo_Paso
    nodo_actual: Optional[str] = None
    vecion_actual: Optional[str] = None
    cola: list = field(default_factory=list)
    visitados: set = field(default_factory=set)
    mensaje : str = ""
    vecinos_analizados: list[str] = field(default_factory=list)

    def __str__(self) -> str:
        if self.mensaje:
            return self.mensaje
        if self.nodo_actual is not None:
            return f"Paso {self.numero}: nodo {self.nodo_actual}"
        return f"Paso {self.numero}"

    def __repr__(self) -> str:
        return self.__str__()