from domain.algorithms.algoritmo_conectividad_grafo import AlgoritmoConectividadGrafo
from domain.Entidades.paso_algoritmo import Paso_Algoritmo, Tipo_Paso


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

        if grafo.get_dirigido:
            self.componentes = self.encontrar_componentes_debilmente_conexas(grafo)

        return grafo.get_matriz()

    def recorrer_desde(self, grafo, origen: str, vecinos=None) -> list[str]:
        """Recorre desde origen siguiendo los vecinos definidos por el grafo."""
        visitados: set[str] = set()
        recorrido: list[str] = []
        pila = [origen]

        while pila:
            nodo = pila.pop()
            if nodo in visitados:
                continue

            visitados.add(nodo)
            recorrido.append(nodo)

            vecinos_nodo = vecinos(nodo) if vecinos is not None else grafo.vecinos(nodo)
            for vecino in reversed(vecinos_nodo):
                if vecino not in visitados:
                    pila.append(vecino)

        return recorrido

    def _adyacencia_debil(self, grafo) -> dict[str, list[str]]:
        adyacencia = {vertice.id: [] for vertice in grafo.vertices}

        for arista in grafo.aristas:
            adyacencia[arista.origen].append(arista.destino)
            adyacencia[arista.destino].append(arista.origen)

        return adyacencia

    def _componentes_con(self, grafo, adyacencia: dict[str, list[str]]) -> list[list[str]]:
        visitados: set[str] = set()
        componentes: list[list[str]] = []

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
                pila.extend(reversed(adyacencia.get(nodo, [])))

            componentes.append(componente)

        return componentes

    def encontrar_componentes_debilmente_conexas(self, grafo) -> list[list[str]]:
        """Componentes del grafo ignorando el sentido de sus aristas."""
        return self._componentes_con(grafo, self._adyacencia_debil(grafo))

    def encontrar_componentes_fuertemente_conexas(self, grafo) -> list[list[str]]:
        """Componentes fuertes mediante el algoritmo Kosaraju."""
        visitados: set[str] = set()
        orden_finalizacion: list[str] = []

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
                for vecino in reversed(grafo.vecinos(nodo)):
                    if vecino not in visitados:
                        pila.append((vecino, False))

        traspuesta: dict[str, list[str]] = {
            vertice.id: [] for vertice in grafo.vertices
        }
        for nodo in grafo.get_lista_adyacencia():
            for vecino in grafo.vecinos(nodo):
                traspuesta[vecino].append(nodo)

        visitados.clear()
        componentes: list[list[str]] = []
        for raiz in reversed(orden_finalizacion):
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
                pila.extend(reversed(traspuesta.get(nodo, [])))

            componentes.append(componente)

        return componentes

    def encontrar_componentes_conexas(self, grafo) -> list[list[str]]:
        if grafo.get_dirigido:
            self.componentes = self.encontrar_componentes_debilmente_conexas(grafo)
            return [componente.copy() for componente in self.componentes]

        self.ejecutar(grafo)
        return [componente.copy() for componente in self.componentes]

    def es_conexo(self, grafo, fuertemente: bool = False) -> bool:
        if grafo.get_dirigido and fuertemente:
            return len(self.encontrar_componentes_fuertemente_conexas(grafo)) == 1
        if grafo.get_dirigido:
            return len(self.encontrar_componentes_debilmente_conexas(grafo)) == 1

        self.ejecutar(grafo)
        return len(self.componentes) == 1