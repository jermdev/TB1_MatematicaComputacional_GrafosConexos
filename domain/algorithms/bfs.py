from collections import deque
from domain.algorithms.algoritmo_conectividad_grafo import AlgoritmoConectividadGrafo
from domain.Entidades.paso_algoritmo import Paso_Algoritmo, Tipo_Paso
from domain.Entidades.grafo import Grafo


class BFS(AlgoritmoConectividadGrafo):
    """
    Algoritmo de búsqueda en anchura (Breadth-First Search - BFS)
    para el análisis de conectividad y determinación de componentes conexas paso a paso.
    """

    def __init__(self, paso_a_paso: bool = False):
        super().__init__(paso_a_paso)
        self.pasos: list[Paso_Algoritmo] = []
        self.componentes: list[list[str]] = []

    def _guardar_paso(
        self,
        tipo: Tipo_Paso,
        visitados: set[str],
        cola: deque[str],
        mensaje: str,
        nodo_actual: str | None = None,
        vecinos_analizados: list[str] | None = None,
    ) -> None:
        self.pasos.append(
            Paso_Algoritmo(
                numero=len(self.pasos) + 1,
                tipo=tipo,
                nodo_actual=nodo_actual,
                cola=list(cola),
                visitados=set(visitados),
                mensaje=mensaje,
                vecinos_analizados=list(vecinos_analizados or []),
            )
        )

    def ejecutar(self, grafo: Grafo) -> list[list[int]]:
        """
        Ejecuta la exploración BFS sobre el grafo, registrando cada paso del recorrido
        y agrupando los vértices en sus componentes conexas.
        """
        self.pasos = []
        self.componentes = []
        visitados: set[str] = set()

        etiq = lambda vid: grafo.obtener_etiqueta(vid) if hasattr(grafo, "obtener_etiqueta") else str(vid)

        for vertice in grafo.vertices:
            raiz = vertice.id
            if raiz in visitados:
                continue

            componente: list[str] = []
            cola = deque([raiz])

            while cola:
                nodo = cola.popleft()
                if nodo in visitados:
                    continue

                visitados.add(nodo)
                componente.append(nodo)
                vecinos_analizados = list(grafo.vecinos(nodo))
                nuevos_vecinos = []
                for vecino in vecinos_analizados:
                    if vecino not in visitados and vecino not in cola:
                        cola.append(vecino)
                        nuevos_vecinos.append(vecino)

                nodo_lbl = etiq(nodo)
                vecinos_lbl = [etiq(v) for v in vecinos_analizados]
                nuevos_lbl = [etiq(v) for v in nuevos_vecinos]

                vecinos_texto = ", ".join(vecinos_lbl) or "ninguno"
                mensaje = f"Se analiza {nodo_lbl}; se revisan sus vecinos: {vecinos_texto}."
                if nuevos_lbl:
                    mensaje += f" Se agregan a la cola: {', '.join(nuevos_lbl)}."
                self._guardar_paso(
                    Tipo_Paso.VISITAR_NODO,
                    visitados,
                    cola,
                    mensaje,
                    nodo,
                    vecinos_analizados,
                )

            self.componentes.append(componente)

        return grafo.get_matriz()

    def encontrar_componentes_conexas(self, grafo: Grafo) -> list[list[str]]:
        """Retorna las componentes conexas identificadas como listas de IDs de vértices."""
        self.ejecutar(grafo)
        return [componente.copy() for componente in self.componentes]

    def es_conexo(self, grafo: Grafo) -> bool:
        """Determina si el grafo tiene exactamente una componente conexa no vacía."""
        self.ejecutar(grafo)
        return len(self.componentes) == 1
