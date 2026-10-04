from algorithms.algoritmo_conectividad_grafo import AlgoritmoConectividadGrafo
from domain.paso_algoritmo import Paso_Algoritmo, Tipo_Paso


class DFS(AlgoritmoConectividadGrafo):
    def __init__(self, paso_a_paso: bool = False):
        super().__init__(paso_a_paso)
        self.pasos: list[Paso_Algoritmo] = []
        self.componentes: list[list[str]] = []

    def _guardar_paso(
        self,
        tipo: Tipo_Paso,
        visitados: set[str],
        pila: list[str],
        mensaje: str,
        nodo_actual: str | None = None,
        vecinos_analizados: list[str] | None = None,
    ) -> None:
        self.pasos.append(
            Paso_Algoritmo(
                numero=len(self.pasos) + 1,
                tipo=tipo,
                nodo_actual=nodo_actual,
                cola=list(pila),
                visitados=set(visitados),
                mensaje=mensaje,
                vecinos_analizados=list(vecinos_analizados or []),
            )
        )

    def ejecutar(self, grafo) -> list[list[int]]:
        self.pasos = []
        self.componentes = []
        visitados: set[str] = set()

        etiq = lambda vid: grafo.obtener_etiqueta(vid) if hasattr(grafo, "obtener_etiqueta") else str(vid)

        for vertice in grafo.vertices:
            raiz = vertice.id
            if raiz in visitados:
                continue

            componente: list[str] = []
            pila = [raiz]

            while pila:
                nodo = pila.pop()
                if nodo in visitados:
                    continue

                visitados.add(nodo)
                componente.append(nodo)
                vecinos_analizados = list(reversed(grafo.vecinos(nodo)))
                nuevos_vecinos = []
                for vecino in vecinos_analizados:
                    if vecino not in visitados and vecino not in pila:
                        pila.append(vecino)
                        nuevos_vecinos.append(vecino)

                nodo_lbl = etiq(nodo)
                vecinos_lbl = [etiq(v) for v in vecinos_analizados]
                nuevos_lbl = [etiq(v) for v in nuevos_vecinos]

                vecinos_texto = ", ".join(vecinos_lbl) or "ninguno"
                mensaje = f"Se analiza {nodo_lbl}; se revisan sus vecinos: {vecinos_texto}."
                if nuevos_lbl:
                    mensaje += f" Se agregan a la pila: {', '.join(nuevos_lbl)}."
                self._guardar_paso(
                    Tipo_Paso.VISITAR_NODO,
                    visitados,
                    pila,
                    mensaje,
                    nodo,
                    vecinos_analizados,
                )

            self.componentes.append(componente)

        return grafo.get_matriz()

    def encontrar_componentes_conexas(self, grafo) -> list[list[str]]:
        self.ejecutar(grafo)
        return [componente.copy() for componente in self.componentes]

    def es_conexo(self, grafo) -> bool:
        self.ejecutar(grafo)
        return len(self.componentes) == 1