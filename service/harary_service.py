from domain.algorithms.harary import Harary
from domain.Entidades.grafo import Grafo
from domain.Entidades.paso_harary import BloqueDiagonalHarary, PasoHarary


class HararyService:
    """
    Servicio especializado para la orquestación y consulta del Algoritmo de Harary.
    Proporciona información estructurada sobre cada matriz generada (adyacencia,
    caminos, filas ordenadas y columnas ordenadas), la navegación paso a paso,
    los cambios y transformaciones entre fases, y la identificación de componentes
    conexas a través de los bloques cuadrados en la diagonal.
    """

    def __init__(self, grafo: Grafo | None = None):
        self.grafo: Grafo | None = grafo
        self.algoritmo: Harary = Harary()
        self.paso_actual: int = 0
        if self.grafo is not None:
            self.ejecutar()

    def set_grafo(self, grafo: Grafo) -> None:
        """Asigna un nuevo grafo y ejecuta el algoritmo automáticamente."""
        self.grafo = grafo
        self.ejecutar()

    def get_grafo(self) -> Grafo | None:
        """Retorna el grafo actual asociado al servicio."""
        return self.grafo

    def ejecutar(self, fuertemente: bool = False) -> Harary:
        """
        Ejecuta el Algoritmo de Harary sobre el grafo actual y reinicia
        el índice de navegación al primer paso.
        """
        if self.grafo is None:
            self.algoritmo = Harary()
            self.paso_actual = 0
            return self.algoritmo

        self.algoritmo = Harary()
        self.algoritmo.ejecutar(self.grafo, fuertemente=fuertemente)
        self.paso_actual = 0
        return self.algoritmo

    def obtener_algoritmo(self) -> Harary:
        """Retorna la instancia del algoritmo con su estado interno."""
        return self.algoritmo

    # -------------------------------------------------------------
    # Navegación y consulta de pasos
    # -------------------------------------------------------------

    def total_pasos(self) -> int:
        """Retorna la cantidad total de pasos registrados."""
        return len(self.algoritmo.pasos)

    def obtener_pasos(self) -> list[PasoHarary]:
        """Retorna la lista completa de pasos generados."""
        return self.algoritmo.pasos

    def obtener_paso(self, indice: int) -> PasoHarary | None:
        """Retorna el paso en el índice indicado o None si está fuera de rango."""
        if 0 <= indice < len(self.algoritmo.pasos):
            return self.algoritmo.pasos[indice]
        return None

    def obtener_paso_actual(self) -> PasoHarary | None:
        """Retorna el paso actualmente activo en la navegación."""
        return self.obtener_paso(self.paso_actual)

    def obtener_indice_paso_actual(self) -> int:
        """Retorna el índice del paso activo."""
        return self.paso_actual

    def ir_a_paso(self, indice: int) -> PasoHarary | None:
        """Fija el paso activo en el índice indicado con validación de límites."""
        total = self.total_pasos()
        if total == 0:
            self.paso_actual = 0
            return None
        self.paso_actual = max(0, min(indice, total - 1))
        return self.obtener_paso_actual()

    def paso_adelante(self) -> int:
        """Avanza al siguiente paso si no se encuentra en el último."""
        total = self.total_pasos()
        if self.paso_actual < total - 1:
            self.paso_actual += 1
        return self.paso_actual

    def paso_atras(self) -> int:
        """Retrocede al paso anterior si no se encuentra en el primero."""
        if self.paso_actual > 0:
            self.paso_actual -= 1
        return self.paso_actual

    # -------------------------------------------------------------
    # Consulta de matrices en cada fase del algoritmo
    # -------------------------------------------------------------

    def obtener_matriz_adyacencia(self) -> dict:
        """
        Retorna la matriz de adyacencia inicial y sus etiquetas asociadas.
        """
        return {
            "matriz": [list(row) for row in self.algoritmo.matriz_adyacencia],
            "etiquetas_filas": list(self.algoritmo.etiquetas_originales),
            "etiquetas_columnas": list(self.algoritmo.etiquetas_originales),
        }

    def obtener_matriz_caminos(self) -> dict:
        """
        Retorna la matriz de caminos (alcanzabilidad) y el conteo de unos por fila.
        """
        return {
            "matriz": [list(row) for row in self.algoritmo.matriz_caminos],
            "etiquetas": list(self.algoritmo.etiquetas_originales),
            "conteo_unos": list(self.algoritmo.conteo_unos),
        }

    def obtener_matriz_filas_ordenadas(self) -> dict:
        """
        Retorna la matriz con filas ordenadas de mayor a menor según cantidad de unos.
        Las columnas aún se encuentran en el orden original.
        """
        return {
            "matriz": [list(row) for row in self.algoritmo.matriz_filas_ordenadas],
            "etiquetas_filas": list(self.algoritmo.etiquetas_ordenadas),
            "etiquetas_columnas": list(self.algoritmo.etiquetas_originales),
            "permutacion": list(self.algoritmo.permutacion),
        }

    def obtener_matriz_columnas_ordenadas(self) -> dict:
        """
        Retorna la matriz final con columnas reordenadas correlativamente a las filas.
        Presenta la estructura diagonal por bloques.
        """
        return {
            "matriz": [list(row) for row in self.algoritmo.matriz_final],
            "etiquetas": list(self.algoritmo.etiquetas_ordenadas),
            "bloques": [b.to_dict() for b in self.algoritmo.bloques_diagonales],
        }

    def obtener_matriz_final(self) -> dict:
        """Alias de obtener_matriz_columnas_ordenadas()."""
        return self.obtener_matriz_columnas_ordenadas()

    # -------------------------------------------------------------
    # Componentes conexas y bloques diagonales
    # -------------------------------------------------------------

    def obtener_componentes_conexas(self) -> list[list[str]]:
        """Retorna las componentes conexas como listas de IDs de vértices."""
        return [list(comp) for comp in self.algoritmo.componentes]

    def obtener_componentes_conexas_etiquetas(self) -> list[list[str]]:
        """Retorna las componentes conexas usando las etiquetas legibles de los vértices."""
        if not self.grafo:
            return []
        etiq = self.grafo.obtener_etiqueta
        return [[etiq(vid) for vid in comp] for comp in self.algoritmo.componentes]

    def obtener_bloques_diagonales(self) -> list[BloqueDiagonalHarary]:
        """Retorna los bloques cuadrados identificados a lo largo de la diagonal."""
        return self.algoritmo.bloques_diagonales

    def es_conexo(self) -> bool:
        """Determina si el grafo analizado es conexo (exactamente una componente conexa)."""
        return len(self.algoritmo.componentes) == 1 and bool(self.grafo and len(self.grafo.vertices) > 0)

    # -------------------------------------------------------------
    # Trazabilidad de cambios y resumen completo
    # -------------------------------------------------------------

    def obtener_cambios_matriz(self) -> list[dict]:
        """
        Genera un historial secuencial descriptivo de las transformaciones que
        experimenta la matriz a lo largo de las distintas fases del algoritmo.
        """
        cambios = []
        for paso in self.algoritmo.pasos:
            cambios.append({
                "numero_paso": paso.numero,
                "fase": paso.tipo.value,
                "titulo": paso.titulo,
                "descripcion": paso.descripcion,
                "dimension": f"{len(paso.matriz)}x{len(paso.matriz[0])}" if paso.matriz else "0x0",
                "etiquetas_filas": list(paso.etiquetas_filas),
                "etiquetas_columnas": list(paso.etiquetas_columnas),
                "detalles": paso.mensaje,
            })
        return cambios

    def obtener_resumen(self) -> dict:
        """
        Genera un resumen integral del análisis realizado por el Algoritmo de Harary,
        preparado para ser consumido directamente por capas de presentación o UI.
        """
        num_v = len(self.grafo.vertices) if self.grafo else 0
        num_e = len(self.grafo.aristas) if self.grafo else 0

        componentes_info = []
        for idx, bloque in enumerate(self.algoritmo.bloques_diagonales, start=1):
            componentes_info.append({
                "componente": idx,
                "tamano": bloque.tamano,
                "vertices_ids": bloque.vertices_ids,
                "vertices_etiquetas": bloque.vertices_etiquetas,
                "coordenadas_bloque": {
                    "fila_inicio": bloque.indice_inicio,
                    "fila_fin": bloque.indice_fin,
                    "columna_inicio": bloque.indice_inicio,
                    "columna_fin": bloque.indice_fin,
                },
            })

        return {
            "num_vertices": num_v,
            "num_aristas": num_e,
            "es_conexo": self.es_conexo(),
            "total_componentes": len(self.algoritmo.componentes),
            "componentes": componentes_info,
            "orden_final_vertices": list(self.algoritmo.etiquetas_ordenadas),
            "permutacion_indices": list(self.algoritmo.permutacion),
            "total_pasos": self.total_pasos(),
            "paso_actual": self.paso_actual,
        }

