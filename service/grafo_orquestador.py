import uuid
from algorithms.dfs import DFS
from algorithms.bfs import BFS
from domain.arista import Arista
from domain.grafo import Grafo
from domain.vertice import Vertice
from service.generador_grafo_service import (
    crear_grafo_ejemplo,
    generar_grafo_aleatorio,
    generar_grafo_vacio,
)


class GrafoOrquestador:
    """
    Clase orquestadora para gestionar el estado del grafo,
    su generación (manual o automática) y la visualización de pasos.
    """

    def __init__(self):
        # Identificador único para el grafo actual (control de persistencia de posiciones)
        self.grafo_id: str = str(uuid.uuid4())
        # Inicializa con el grafo de ejemplo
        self.grafo: Grafo = crear_grafo_ejemplo()
        self.modo: str = "Automático"
        self.num_vertices: int = 4
        self.algoritmo_seleccionado: str = "DFS"
        self.vista_actual: str = "grafo"  # 'grafo' o 'matriz'
        self.pasos_algoritmo: list = []
        self.componentes_conexas: list[list[str]] = []
        self.pasos: list = []
        self.paso_actual: int = 0
        self.ultimo_mensaje: str = ""
        self.actualizar_algoritmo(paso_inicial=0)

    def generar_grafo(
        self,
        num_vertices: int,
        modo: str = "Automático",
        algoritmo: str = "DFS",
        probabilidad: float = 0.35,
        dirigido: bool = False,
    ) -> Grafo:
        """
        Genera un nuevo grafo según los parámetros de configuración.
        El índice de paso se inicializa siempre en el primer paso (paso 0).
        Se actualiza self.grafo_id para reiniciar la disposición física de los vértices.
        """
        self.grafo_id = str(uuid.uuid4())
        self.num_vertices = max(1, num_vertices)
        self.modo = modo
        self.algoritmo_seleccionado = algoritmo

        if modo == "Automático":
            self.grafo = generar_grafo_aleatorio(
                num_vertices=self.num_vertices,
                probabilidad=probabilidad,
                dirigido=dirigido,
            )
            total_aristas = len(self.grafo.aristas)
            self.ultimo_mensaje = f"Grafo automático generado ({self.num_vertices} vértices, {total_aristas} aristas)."
        else:
            # Modo manual: se crean los vértices limpios para conectar
            self.grafo = generar_grafo_vacio(
                num_vertices=self.num_vertices,
                dirigido=dirigido,
            )
            self.ultimo_mensaje = f"Modo manual activado con {self.num_vertices} vértices. Agrega aristas."

        self.actualizar_algoritmo(paso_inicial=0)
        self.paso_actual = 0
        return self.grafo

    def cambiar_modo(self, modo: str):
        """Actualiza el modo actual (Automático o Manual)."""
        self.modo = modo

    def obtener_etiqueta_vertice(self, vertice_id: str) -> str:
        """Retorna la etiqueta legible o el id de un vértice."""
        if self.grafo:
            return self.grafo.obtener_etiqueta(vertice_id)
        return str(vertice_id)

    def existe_conexion(self, origen_id: str, destino_id: str) -> bool:
        """Verifica si ya existe una arista entre dos vértices en el grafo."""
        if not self.grafo:
            return False
        return self.grafo.existe_arista(origen_id, destino_id)

    def actualizar_algoritmo(self, paso_inicial: int | None = None):
        """
        Recalcula los pasos del algoritmo y los componentes conexos
        para reflejar el estado actual del grafo.
        """
        if not self.grafo:
            return

        if self.algoritmo_seleccionado == "DFS":
            algoritmo_obj = DFS()
            algoritmo_obj.ejecutar(self.grafo)
            self.pasos_algoritmo = algoritmo_obj.pasos
            self.componentes_conexas = [componente.copy() for componente in algoritmo_obj.componentes]
            self.pasos = list(algoritmo_obj.pasos)
        elif self.algoritmo_seleccionado == "BFS":
            algoritmo_obj = BFS()
            algoritmo_obj.ejecutar(self.grafo)
            self.pasos_algoritmo = algoritmo_obj.pasos
            self.componentes_conexas = [componente.copy() for componente in algoritmo_obj.componentes]
            self.pasos = list(algoritmo_obj.pasos)
        else:
            self.pasos_algoritmo = []
            self.componentes_conexas = []
            self.pasos = [
                f"Grafo con {len(self.grafo.vertices)} vértices y {len(self.grafo.aristas)} aristas.",
                f"Algoritmo: {self.algoritmo_seleccionado}.",
            ]

        if paso_inicial is not None:
            self.paso_actual = paso_inicial
        else:
            self.paso_actual = min(getattr(self, "paso_actual", 0), max(0, len(self.pasos) - 1))

    def agregar_conexion_manual(
        self,
        origen_id: str,
        destino_id: str,
        peso: float = 1.0,
        dirigida: bool = False,
    ) -> tuple[bool, str]:
        """
        Agrega una arista manualmente entre dos vértices del grafo actual.
        Valida que no exista previamente y actualiza el análisis de componentes conexas.
        """
        if not self.grafo:
            return False, "No hay ningún grafo inicializado."

        u, v = str(origen_id), str(destino_id)
        if u == v:
            return False, "No se permiten bucles (origen y destino deben ser distintos)."

        vertices_dict = {str(vert.id): vert for vert in self.grafo.vertices}
        if u not in vertices_dict or v not in vertices_dict:
            return False, "Uno o ambos vértices no existen en el grafo actual."

        # Verificar si la conexión ya existe
        if self.existe_conexion(u, v):
            etiqueta_orig = self.obtener_etiqueta_vertice(u)
            etiqueta_dest = self.obtener_etiqueta_vertice(v)
            return False, f"La conexión entre {etiqueta_orig} y {etiqueta_dest} ya existe."

        nueva_arista = Arista(
            origen=u,
            destino=v,
            peso=peso,
            dirigida=dirigida,
        )
        self.grafo.agregar_arista(nueva_arista)
        self.actualizar_algoritmo()

        etiqueta_orig = self.obtener_etiqueta_vertice(u)
        etiqueta_dest = self.obtener_etiqueta_vertice(v)
        simbolo = "→" if (dirigida or self.grafo.dirigido) else "↔"
        msg = f"Conexión agregada: {etiqueta_orig} {simbolo} {etiqueta_dest}"

        self.ultimo_mensaje = msg
        return True, msg

    def eliminar_conexion_manual(self, origen_id: str, destino_id: str) -> tuple[bool, str]:
        """
        Elimina una arista existente entre dos vértices.
        """
        if not self.grafo:
            return False, "No hay ningún grafo activo."

        u, v = str(origen_id), str(destino_id)
        aristas_nuevas = []
        encontrada = False
        es_dirigido = self.grafo.dirigido

        for a in self.grafo._aristas:
            coincide = (a.origen == u and a.destino == v)
            if not es_dirigido and not a.dirigida:
                coincide = coincide or (a.origen == v and a.destino == u)

            if coincide:
                encontrada = True
            else:
                aristas_nuevas.append(a)

        if not encontrada:
            return False, f"No se encontró arista entre {u} y {v}."

        self.grafo._aristas = aristas_nuevas
        # Reconstruir listas de adyacencia
        self.grafo._adyacencia = {vert.id: [] for vert in self.grafo.vertices}
        for a in self.grafo._aristas:
            self.grafo._adyacencia[a.origen].append(a.destino)
            if not (a.dirigida or self.grafo.dirigido):
                self.grafo._adyacencia[a.destino].append(a.origen)

        self.actualizar_algoritmo()
        etiqueta_orig = self.obtener_etiqueta_vertice(u)
        etiqueta_dest = self.obtener_etiqueta_vertice(v)
        msg = f"Conexión cancelada: {etiqueta_orig} ↔ {etiqueta_dest} eliminada."
        self.ultimo_mensaje = msg
        return True, msg

    def cancelar_ultima_conexion(self) -> tuple[bool, str]:
        """
        Elimina la última arista agregada al grafo (opción de cancelar/deshacer).
        """
        if not self.grafo or not self.grafo.aristas:
            return False, "No hay conexiones activas para cancelar."

        ultima = self.grafo.aristas[-1]
        return self.eliminar_conexion_manual(ultima.origen, ultima.destino)

    def limpiar_conexiones(self):
        """Elimina todas las aristas del grafo manteniendo sus vértices."""
        if self.grafo:
            self.grafo._aristas = []
            self.grafo._adyacencia = {v.id: [] for v in self.grafo.vertices}
            self.actualizar_algoritmo()
            self.ultimo_mensaje = "Todas las conexiones fueron eliminadas."

    def alternar_vista(self) -> str:
        """Alterna entre vista de grafo y vista de matriz de adyacencia."""
        self.vista_actual = "matriz" if self.vista_actual == "grafo" else "grafo"
        return self.vista_actual

    def cambiar_vista(self, vista: str):
        if vista in ("grafo", "matriz"):
            self.vista_actual = vista

    def paso_adelante(self):
        if self.paso_actual < len(self.pasos) - 1:
            self.paso_actual += 1

    def paso_atras(self):
        if self.paso_actual > 0:
            self.paso_actual -= 1

    def obtener_grafo(self) -> Grafo:
        return self.grafo

    def obtener_matriz(self) -> list[list[int]]:
        return self.grafo.get_matriz() if self.grafo else []
