from dataclasses import dataclass, field
from enum import Enum


class TipoPasoHarary(str, Enum):
    MATRIZ_ADYACENCIA = "MATRIZ_ADYACENCIA"
    MATRIZ_CAMINOS = "MATRIZ_CAMINOS"
    ORDENAR_FILAS = "ORDENAR_FILAS"
    ORDENAR_COLUMNAS = "ORDENAR_COLUMNAS"
    IDENTIFICAR_BLOQUES = "IDENTIFICAR_BLOQUES"
    RESUMEN = "RESUMEN"


@dataclass
class BloqueDiagonalHarary:
    """
    Representa un bloque cuadrado de unos a lo largo de la diagonal principal
    de la matriz permutada simétricamente en el Algoritmo de Harary.
    Cada bloque corresponde a una componente conexa del grafo.
    """
    numero_componente: int
    indice_inicio: int
    indice_fin: int
    tamano: int
    vertices_ids: list[str] = field(default_factory=list)
    vertices_etiquetas: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "numero_componente": self.numero_componente,
            "indice_inicio": self.indice_inicio,
            "indice_fin": self.indice_fin,
            "tamano": self.tamano,
            "vertices_ids": list(self.vertices_ids),
            "vertices_etiquetas": list(self.vertices_etiquetas),
        }


@dataclass
class PasoHarary:
    """
    Representa el estado del Algoritmo de Harary en una fase específica,
    almacenando la matriz resultante en ese instante, las etiquetas de
    filas y columnas, el mapeo de reordenamiento y los bloques identificados.
    """
    numero: int
    tipo: TipoPasoHarary
    titulo: str
    descripcion: str
    mensaje: str
    matriz: list[list[int]]
    etiquetas_filas: list[str]
    etiquetas_columnas: list[str]
    conteo_unos: list[int] = field(default_factory=list)
    permutacion_indices: list[int] = field(default_factory=list)
    mapeo_filas: list[dict] = field(default_factory=list)
    mapeo_columnas: list[dict] = field(default_factory=list)
    bloques_diagonales: list[BloqueDiagonalHarary] = field(default_factory=list)
    componentes: list[list[str]] = field(default_factory=list)
    es_conexo: bool = False

    def __str__(self) -> str:
        return f"Paso {self.numero} ({self.titulo}): {self.mensaje}"

    def __repr__(self) -> str:
        return self.__str__()

    def to_dict(self) -> dict:
        return {
            "numero": self.numero,
            "tipo": self.tipo.value if isinstance(self.tipo, TipoPasoHarary) else str(self.tipo),
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "mensaje": self.mensaje,
            "matriz": [list(row) for row in self.matriz],
            "etiquetas_filas": list(self.etiquetas_filas),
            "etiquetas_columnas": list(self.etiquetas_columnas),
            "conteo_unos": list(self.conteo_unos),
            "permutacion_indices": list(self.permutacion_indices),
            "mapeo_filas": list(self.mapeo_filas),
            "mapeo_columnas": list(self.mapeo_columnas),
            "bloques_diagonales": [b.to_dict() for b in self.bloques_diagonales],
            "componentes": [list(c) for c in self.componentes],
            "es_conexo": self.es_conexo,
        }

