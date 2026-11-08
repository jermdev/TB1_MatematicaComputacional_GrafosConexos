from domain.algorithms.algoritmo_conectividad_grafo import AlgoritmoConectividadGrafo
from domain.Entidades.grafo import Grafo
from domain.Entidades.paso_harary import BloqueDiagonalHarary, PasoHarary, TipoPasoHarary


class Harary(AlgoritmoConectividadGrafo):
    """
    Algoritmo de Harary para el análisis de conectividad y determinación de
    componentes conexas a través de transformaciones sobre la matriz de caminos.

    Procedimiento:
    1. Construcción de la matriz de adyacencia inicial.
    2. Obtención de la matriz de caminos (alcanzabilidad) mediante clausura
       transitiva (Warshall) con reflexividad en la diagonal principal.
    3. Conteo de unos en cada fila y ordenamiento descendente de las filas (las
       filas con más unos se colocan primero).
    4. Reordenamiento correlativo de las columnas aplicando exactamente la misma
       permutación de las filas.
    5. Identificación de los bloques cuadrados de unos a lo largo de la diagonal
       principal, donde cada cuadrado representa una componente conexa del grafo.
    """

    def __init__(self, paso_a_paso: bool = False):
        super().__init__(paso_a_paso)
        self.pasos: list[PasoHarary] = []
        self.componentes: list[list[str]] = []
        self.bloques_diagonales: list[BloqueDiagonalHarary] = []
        self.matriz_adyacencia: list[list[int]] = []
        self.matriz_caminos: list[list[int]] = []
        self.matriz_filas_ordenadas: list[list[int]] = []
        self.matriz_final: list[list[int]] = []
        self.permutacion: list[int] = []
        self.conteo_unos: list[int] = []
        self.etiquetas_originales: list[str] = []
        self.etiquetas_ordenadas: list[str] = []

    def ejecutar(self, grafo: Grafo, fuertemente: bool = True) -> list[list[int]]:
        """
        Ejecuta el Algoritmo de Harary sobre el grafo dado, generando la bitácora
        de pasos matriciales, los bloques cuadrados en la diagonal y las
        componentes conexas identificadas.
        """
        self.pasos = []
        self.componentes = []
        self.bloques_diagonales = []

        vertices = grafo.vertices
        n = len(vertices)

        if n == 0:
            self.matriz_adyacencia = []
            self.matriz_caminos = []
            self.matriz_filas_ordenadas = []
            self.matriz_final = []
            self.permutacion = []
            self.conteo_unos = []
            self.etiquetas_originales = []
            self.etiquetas_ordenadas = []
            return []

        ids_originales = [str(v.id) for v in vertices]
        etiquetas_originales = [grafo.obtener_etiqueta(v.id) for v in vertices]
        self.etiquetas_originales = list(etiquetas_originales)

        # -------------------------------------------------------------
        # PASO 1: Matriz de Adyacencia
        # -------------------------------------------------------------
        A_raw = grafo.get_matriz()
        self.matriz_adyacencia = [list(fila) for fila in A_raw]

        paso_1 = PasoHarary(
            numero=1,
            tipo=TipoPasoHarary.MATRIZ_ADYACENCIA,
            titulo="Matriz de Adyacencia Inicial",
            descripcion=(
                "Se obtiene la matriz de adyacencia del grafo donde A[i][j] = 1 indica "
                "la existencia de una arista directa entre el vértice i y el vértice j."
            ),
            mensaje=(
                f"Matriz de adyacencia construida con {n} vértices y "
                f"{len(grafo.aristas)} aristas ({'dirigido' if grafo.dirigido else 'no dirigido'})."
            ),
            matriz=[list(row) for row in self.matriz_adyacencia],
            etiquetas_filas=list(etiquetas_originales),
            etiquetas_columnas=list(etiquetas_originales),
        )
        self.pasos.append(paso_1)

        # -------------------------------------------------------------
        # PASO 2: Matriz de Caminos (Alcanzabilidad) y Conteo de Unos
        # -------------------------------------------------------------
        # Si el grafo es dirigido y fuertemente=True, evaluamos transitividad dirigida
        # respetando la dirección de las aristas.
        # Si fuertemente=False en un grafo dirigido, se evalúa conectividad débil.
        # En grafos no dirigidos, la matriz de adyacencia ya es intrínsecamente simétrica.
        if grafo.dirigido and fuertemente:
            A_base = [list(fila) for fila in self.matriz_adyacencia]
            tipo_eval = "dirigido (conectividad fuerte)"
        elif grafo.dirigido and not fuertemente:
            A_base = [
                [
                    1 if (self.matriz_adyacencia[i][j] == 1 or self.matriz_adyacencia[j][i] == 1) else 0
                    for j in range(n)
                ]
                for i in range(n)
            ]
            tipo_eval = "dirigido evaluado como no dirigido (conectividad débil)"
        else:
            A_base = [list(fila) for fila in self.matriz_adyacencia]
            tipo_eval = "no dirigido"

        # Clausura transitiva con diagonal reflexiva (algoritmo de Warshall)
        P = [
            [1 if i == j or A_base[i][j] != 0 else 0 for j in range(n)]
            for i in range(n)
        ]
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    P[i][j] = 1 if (P[i][j] == 1 or (P[i][k] == 1 and P[k][j] == 1)) else 0

        self.matriz_caminos = [list(fila) for fila in P]
        conteo_unos = [sum(P[i]) for i in range(n)]
        self.conteo_unos = list(conteo_unos)

        detalle_unos = ", ".join(
            f"{etiquetas_originales[i]}={conteo_unos[i]}" for i in range(n)
        )
        paso_2 = PasoHarary(
            numero=2,
            tipo=TipoPasoHarary.MATRIZ_CAMINOS,
            titulo="Matriz de Caminos (Alcanzabilidad)",
            descripcion=(
                f"Se calcula la matriz de caminos con diagonal reflexiva mediante "
                f"clausura transitiva ({tipo_eval}). Para cada fila se contabiliza el número total de unos."
            ),
            mensaje=(
                f"Matriz de caminos calculada ({tipo_eval}). Conteo de unos por fila: {detalle_unos}."
            ),
            matriz=[list(row) for row in self.matriz_caminos],
            etiquetas_filas=list(etiquetas_originales),
            etiquetas_columnas=list(etiquetas_originales),
            conteo_unos=list(conteo_unos),
        )
        self.pasos.append(paso_2)

        # -------------------------------------------------------------
        # PASO 3: Ordenar las Filas por Cantidad de Unos (Mayor a Menor)
        # -------------------------------------------------------------
        # Para que los vértices de una misma componente queden contiguos sin
        # dispersarse, agrupamos por el vector de fila (que es idéntico para
        # todos los nodos de la misma componente conexa).
        primer_avistamiento: dict[tuple, int] = {}
        for i in range(n):
            patron = tuple(P[i])
            if patron not in primer_avistamiento:
                primer_avistamiento[patron] = i

        permutacion = sorted(
            range(n),
            key=lambda i: (-conteo_unos[i], primer_avistamiento[tuple(P[i])], i),
        )
        self.permutacion = list(permutacion)
        etiquetas_ordenadas = [etiquetas_originales[p] for p in permutacion]
        self.etiquetas_ordenadas = list(etiquetas_ordenadas)

        M_filas = [P[p].copy() for p in permutacion]
        self.matriz_filas_ordenadas = [list(row) for row in M_filas]

        mapeo_filas = [
            {
                "etiqueta": etiquetas_originales[p],
                "pos_original": p,
                "nueva_pos": r,
                "unos": conteo_unos[p],
            }
            for r, p in enumerate(permutacion)
        ]

        desc_mapeo_filas = ", ".join(
            f"{m['etiqueta']} (f{m['pos_original'] + 1} → f{m['nueva_pos'] + 1}, {m['unos']} unos)"
            for m in mapeo_filas
        )

        paso_3 = PasoHarary(
            numero=3,
            tipo=TipoPasoHarary.ORDENAR_FILAS,
            titulo="Ordenamiento de Filas por Unos",
            descripcion=(
                "Se ordenan las filas de mayor a menor cantidad de unos. Las filas con "
                "más conexiones se ubican en las primeras posiciones."
            ),
            mensaje=(
                f"Filas reordenadas según número de unos: {desc_mapeo_filas}."
            ),
            matriz=[list(row) for row in self.matriz_filas_ordenadas],
            etiquetas_filas=list(etiquetas_ordenadas),
            etiquetas_columnas=list(etiquetas_originales),
            conteo_unos=[conteo_unos[p] for p in permutacion],
            permutacion_indices=list(permutacion),
            mapeo_filas=mapeo_filas,
        )
        self.pasos.append(paso_3)

        # -------------------------------------------------------------
        # PASO 4: Ordenar las Columnas en el Mismo Orden de las Filas
        # -------------------------------------------------------------
        # Si la fila que era la posición 5 ahora está en la posición 1,
        # la columna 5 pasa exactamente a la posición 1.
        M_final = [[M_filas[r][c] for c in permutacion] for r in range(n)]
        self.matriz_final = [list(row) for row in M_final]

        mapeo_columnas = [
            {
                "etiqueta": etiquetas_originales[p],
                "pos_original": p,
                "nueva_pos": c,
            }
            for c, p in enumerate(permutacion)
        ]

        desc_mapeo_columnas = ", ".join(
            f"{m['etiqueta']} (c{m['pos_original'] + 1} → c{m['nueva_pos'] + 1})"
            for m in mapeo_columnas
        )

        paso_4 = PasoHarary(
            numero=4,
            tipo=TipoPasoHarary.ORDENAR_COLUMNAS,
            titulo="Ordenamiento Correlativo de Columnas",
            descripcion=(
                "Se reordenan las columnas en el mismo orden que las filas de unos. "
                "Si la fila en posición original i pasó a la posición j, la columna i "
                "pasa también a la posición j, obteniendo una matriz diagonal por bloques."
            ),
            mensaje=(
                f"Columnas reordenadas simétricamente: {desc_mapeo_columnas}."
            ),
            matriz=[list(row) for row in self.matriz_final],
            etiquetas_filas=list(etiquetas_ordenadas),
            etiquetas_columnas=list(etiquetas_ordenadas),
            permutacion_indices=list(permutacion),
            mapeo_columnas=mapeo_columnas,
        )
        self.pasos.append(paso_4)

        # -------------------------------------------------------------
        # PASO 5: Identificación de Cuadrados en la Diagonal
        # -------------------------------------------------------------
        bloques: list[BloqueDiagonalHarary] = []
        componentes: list[list[str]] = []

        idx = 0
        num_componente = 1
        while idx < n:
            # Encontrar el tamaño máximo del bloque cuadrado de unos a lo largo de la diagonal
            tamano = 1
            while idx + tamano < n:
                siguiente_tam = tamano + 1
                es_cuadrado = all(
                    M_final[idx + r][idx + c] == 1
                    for r in range(siguiente_tam)
                    for c in range(siguiente_tam)
                )
                if es_cuadrado:
                    tamano = siguiente_tam
                else:
                    break

            indices_bloque = [permutacion[k] for k in range(idx, idx + tamano)]
            verts_ids = [ids_originales[p] for p in indices_bloque]
            verts_etiqs = [etiquetas_originales[p] for p in indices_bloque]

            bloque = BloqueDiagonalHarary(
                numero_componente=num_componente,
                indice_inicio=idx,
                indice_fin=idx + tamano - 1,
                tamano=tamano,
                vertices_ids=verts_ids,
                vertices_etiquetas=verts_etiqs,
            )
            bloques.append(bloque)
            componentes.append(verts_ids)

            idx += tamano
            num_componente += 1

        self.bloques_diagonales = bloques
        self.componentes = componentes

        desc_bloques = "; ".join(
            f"Componente {b.numero_componente} (bloque {b.tamano}x{b.tamano}, "
            f"filas/cols {b.indice_inicio + 1} a {b.indice_fin + 1}): {{{', '.join(b.vertices_etiquetas)}}}"
            for b in bloques
        )

        paso_5 = PasoHarary(
            numero=5,
            tipo=TipoPasoHarary.IDENTIFICAR_BLOQUES,
            titulo="Identificación de Cuadrados en la Diagonal",
            descripcion=(
                "Se identifican los bloques cuadrados de unos a lo largo de la diagonal principal. "
                "Cada bloque cuadrado representa exactamente una componente conexa del grafo."
            ),
            mensaje=(
                f"Se identificaron {len(bloques)} cuadrado(s) en la diagonal principal: {desc_bloques}."
            ),
            matriz=[list(row) for row in self.matriz_final],
            etiquetas_filas=list(etiquetas_ordenadas),
            etiquetas_columnas=list(etiquetas_ordenadas),
            bloques_diagonales=list(bloques),
            componentes=[list(c) for c in componentes],
            es_conexo=(len(componentes) == 1),
        )
        self.pasos.append(paso_5)

        # -------------------------------------------------------------
        # PASO 6: Diagnóstico y Resumen Final
        # -------------------------------------------------------------
        es_conexo_grafo = (len(componentes) == 1)
        if grafo.dirigido:
            if fuertemente:
                tipo_con_nom = "fuertemente conexas"
                estado_conexo = (
                    "FUERTEMENTE CONEXO (1 componente fuertemente conexa)"
                    if es_conexo_grafo
                    else f"NO FUERTEMENTE CONEXO ({len(componentes)} componentes fuertemente conexas)"
                )
            else:
                tipo_con_nom = "débilmente conexas"
                estado_conexo = (
                    "DÉBILMENTE CONEXO (1 componente débilmente conexa)"
                    if es_conexo_grafo
                    else f"DISCONEXO ({len(componentes)} componentes débilmente conexas)"
                )
        else:
            tipo_con_nom = "conexas"
            estado_conexo = (
                "CONEXO (1 componente conexa)"
                if es_conexo_grafo
                else f"DISCONEXO ({len(componentes)} componentes conexas)"
            )

        paso_6 = PasoHarary(
            numero=6,
            tipo=TipoPasoHarary.RESUMEN,
            titulo="Diagnóstico Final de Conectividad",
            descripcion=(
                "Resumen de conectividad global del grafo según el análisis de bloques "
                "diagonales del Algoritmo de Harary."
            ),
            mensaje=(
                f"Análisis completado: el grafo es {estado_conexo}. "
                f"Total de componentes {tipo_con_nom}: {len(componentes)}."
            ),
            matriz=[list(row) for row in self.matriz_final],
            etiquetas_filas=list(etiquetas_ordenadas),
            etiquetas_columnas=list(etiquetas_ordenadas),
            bloques_diagonales=list(bloques),
            componentes=[list(c) for c in componentes],
            es_conexo=es_conexo_grafo,
        )
        self.pasos.append(paso_6)

        return [list(row) for row in self.matriz_final]

    def encontrar_componentes_conexas(self, grafo: Grafo, fuertemente: bool = True) -> list[list[str]]:
        """Retorna las componentes conexas identificadas como listas de IDs de vértices."""
        self.ejecutar(grafo, fuertemente=fuertemente)
        return [componente.copy() for componente in self.componentes]

    def encontrar_componentes_fuertemente_conexas(self, grafo: Grafo) -> list[list[str]]:
        """Retorna las componentes fuertemente conexas de un grafo dirigido."""
        self.ejecutar(grafo, fuertemente=True)
        return [componente.copy() for componente in self.componentes]

    def encontrar_componentes_debilmente_conexas(self, grafo: Grafo) -> list[list[str]]:
        """Retorna las componentes débilmente conexas de un grafo dirigido."""
        self.ejecutar(grafo, fuertemente=False)
        return [componente.copy() for componente in self.componentes]

    def es_conexo(self, grafo: Grafo, fuertemente: bool = True) -> bool:
        """Determina si el grafo tiene exactamente una componente conexa no vacía."""
        self.ejecutar(grafo, fuertemente=fuertemente)
        return len(self.componentes) == 1

