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

    def _es_dirigido(self, grafo: Grafo) -> bool:
        """Función auxiliar para evaluar de forma segura si el grafo es dirigido."""
        if hasattr(grafo, "get_dirigido"):
            attr = getattr(grafo, "get_dirigido")
            # Soporta tanto si get_dirigido es un método get_dirigido() o una propiedad booleana
            return attr() if callable(attr) else bool(attr)
        return False

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

        if self._es_dirigido(grafo):
            self.componentes = self.encontrar_componentes_debilmente_conexas(grafo)

        return grafo.get_matriz()

    def recorrer_desde(self, grafo: Grafo, origen: str, vecinos=None) -> list[str]:
        visitados: set[str] = set()
        recorrido: list[str] = []
        cola = deque([origen])

        while cola:
            nodo = cola.popleft()
            if nodo in visitados:
                continue

            visitados.add(nodo)
            recorrido.append(nodo)

            vecinos_nodo = vecinos(nodo) if vecinos is not None else grafo.vecinos(nodo)
            for vecino in vecinos_nodo:
                if vecino not in visitados and vecino not in cola:
                    cola.append(vecino)

        return recorrido

    def _adyacencia_debil(self, grafo: Grafo) -> dict[str, list[str]]:
        adyacencia = {vertice.id: [] for vertice in grafo.vertices}

        for arista in grafo.aristas:
            adyacencia[arista.origen].append(arista.destino)
            adyacencia[arista.destino].append(arista.origen)

        return adyacencia

    def _componentes_con(self, grafo: Grafo, adyacencia: dict[str, list[str]]) -> list[list[str]]:
        visitados: set[str] = set()
        componentes: list[list[str]] = []

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
                
                for vecino in adyacencia.get(nodo, []):
                    if vecino not in visitados and vecino not in cola:
                        cola.append(vecino)

            componentes.append(componente)

        return componentes

    def encontrar_componentes_debilmente_conexas(self, grafo: Grafo) -> list[list[str]]:
        return self._componentes_con(grafo, self._adyacencia_debil(grafo))

    def encontrar_componentes_fuertemente_conexas(self, grafo: Grafo) -> list[list[str]]:
        visitados: set[str] = set()
        orden_finalizacion: list[str] = []

        # Paso 1 de Kosaraju (DFS estricto para orden de finalización)
        for vertice in grafo.vertices:
            raiz = vertice.id
            if raiz in visitados:
                continue

            pila = [(raiz, False)]
            while pila:
                nodo, finalizado = pila.pop()
                if finalizado:
                    orden_finalizacion.append(nodo)
                    continue
                if nodo in visitados:
                    continue

                visitados.add(nodo)
                pila.append((nodo, True))
                for vecino in reversed(list(grafo.vecinos(nodo))):
                    if vecino not in visitados:
                        pila.append((vecino, False))

        traspuesta: dict[str, list[str]] = {
            vertice.id: [] for vertice in grafo.vertices
        }
        for nodo in grafo.get_lista_adyacencia():
            for vecino in grafo.vecinos(nodo):
                traspuesta[vecino].append(nodo)

        # Paso 2 de Kosaraju adaptado a BFS
        visitados.clear()
        componentes: list[list[str]] = []
        for raiz in reversed(orden_finalizacion):
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
                for vecino in traspuesta.get(nodo, []):
                    if vecino not in visitados and vecino not in cola:
                        cola.append(vecino)

            componentes.append(componente)

        return componentes

    # --- ZONA CORREGIDA (En torno a las últimas líneas) ---

    def encontrar_componentes_conexas(self, grafo: Grafo) -> list[list[str]]:
        """Retorna las componentes conexas identificadas como listas de IDs de vértices."""
        if self._es_dirigido(grafo):
            self.componentes = self.encontrar_componentes_debilmente_conexas(grafo)
        else:
            self.ejecutar(grafo)
            
        return [componente.copy() for componente in self.componentes]

    def es_conexo(self, grafo: Grafo, fuertemente: bool = False) -> bool:
        """Determina si el grafo tiene exactamente una componente conexa no vacía."""
        if self._es_dirigido(grafo):
            if fuertemente:
                self.componentes = self.encontrar_componentes_fuertemente_conexas(grafo)
            else:
                self.componentes = self.encontrar_componentes_debilmente_conexas(grafo)
        else:
            self.ejecutar(grafo)

        # Ahora todo el flujo aterriza correctamente en esta última línea, 
        # garantizando que 'self.componentes' fue actualizado según el caso.
        return len(self.componentes) == 1