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
        # Inicializa con el grafo de ejemplo
        self.grafo: Grafo = crear_grafo_ejemplo()
        self.modo: str = "Automático"
        self.num_vertices: int = 4
        self.algoritmo_seleccionado: str = "DFS"
        self.vista_actual: str = "grafo"  # 'grafo' o 'matriz'
        self.pasos: list[str] = [
            "Sistema iniciado: Grafo base listo.",
            "Selecciona la configuración y presiona 'Generar grafo' para comenzar.",
        ]
        self.paso_actual: int = 0
        self.ultimo_mensaje: str = ""

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
        """
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
            self.pasos = [
                f"Paso 1: Generación automática completada con {self.num_vertices} vértices y {total_aristas} aristas.",
                f"Paso 2: Algoritmo configurado para análisis: {algoritmo}.",
                "Paso 3: Grafo listo para iniciar el recorrido de componentes conexas.",
            ]
            self.ultimo_mensaje = f"Grafo automático generado ({self.num_vertices} vértices, {total_aristas} aristas)."
        else:
            # Modo manual: se crean los vértices limpios para conectar
            self.grafo = generar_grafo_vacio(
                num_vertices=self.num_vertices,
                dirigido=dirigido,
            )
            self.pasos = [
                f"Paso 1: Vértices inicializados ({self.num_vertices}) para modo manual.",
                "Paso 2: Conecta vértices usando los selectores o interactuando en el canvas.",
                f"Paso 3: Algoritmo seleccionado: {algoritmo}.",
            ]
            self.ultimo_mensaje = f"Modo manual activado con {self.num_vertices} vértices. Agrega aristas."

        self.paso_actual = 0
        return self.grafo

    def agregar_conexion_manual(
        self,
        origen_id: str,
        destino_id: str,
        peso: float = 1.0,
        dirigida: bool = False,
    ) -> tuple[bool, str]:
        """
        Agrega una arista manualmente entre dos vértices del grafo actual.
        """
        if not self.grafo:
            return False, "No hay ningún grafo inicializado."

        if origen_id == destino_id:
            return False, "No se permiten bucles (origen y destino deben ser distintos)."

        vertices_dict = {v.id: v for v in self.grafo.vertices}
        if origen_id not in vertices_dict or destino_id not in vertices_dict:
            return False, "Uno o ambos vértices no existen en el grafo actual."

        # Verificar si la arista ya existe
        es_grafo_dirigido = dirigida or self.grafo.dirigido
        for a in self.grafo.aristas:
            if a.origen == origen_id and a.destino == destino_id:
                return False, f"La arista ({origen_id} -> {destino_id}) ya existe."
            if not es_grafo_dirigido and a.origen == destino_id and a.destino == origen_id:
                return False, f"La arista entre {origen_id} y {destino_id} ya existe."

        nueva_arista = Arista(
            origen=origen_id,
            destion=destino_id,
            peso=peso,
            dirigida=dirigida,
        )
        self.grafo.agregar_arista(nueva_arista)

        etiqueta_orig = vertices_dict[origen_id].etiqueta or origen_id
        etiqueta_dest = vertices_dict[destino_id].etiqueta or destino_id
        simbolo = "→" if es_grafo_dirigido else "↔"
        msg = f"Conexión agregada: {etiqueta_orig} ({origen_id}) {simbolo} {etiqueta_dest} ({destino_id})"

        self.pasos.append(msg)
        self.paso_actual = len(self.pasos) - 1
        self.ultimo_mensaje = msg
        return True, msg

    def eliminar_conexion_manual(self, origen_id: str, destino_id: str) -> tuple[bool, str]:
        """
        Elimina una arista existente entre dos vértices.
        """
        if not self.grafo:
            return False, "No hay ningún grafo activo."

        aristas_nuevas = []
        encontrada = False
        es_dirigido = self.grafo.dirigido

        for a in self.grafo._aristas:
            coincide = (a.origen == origen_id and a.destino == destino_id)
            if not es_dirigido and not a.dirigida:
                coincide = coincide or (a.origen == destino_id and a.destino == origen_id)

            if coincide:
                encontrada = True
            else:
                aristas_nuevas.append(a)

        if not encontrada:
            return False, f"No se encontró arista entre {origen_id} y {destino_id}."

        self.grafo._aristas = aristas_nuevas
        # Reconstruir listas de adyacencia
        self.grafo._adyacencia = {v.id: [] for v in self.grafo.vertices}
        for a in self.grafo._aristas:
            self.grafo._adyacencia[a.origen].append(a.destino)
            if not (a.dirigida or self.grafo.dirigido):
                self.grafo._adyacencia[a.destino].append(a.origen)

        msg = f"Conexión eliminada entre {origen_id} y {destino_id}."
        self.pasos.append(msg)
        self.paso_actual = len(self.pasos) - 1
        self.ultimo_mensaje = msg
        return True, msg

    def limpiar_conexiones(self):
        """Elimina todas las aristas del grafo manteniendo sus vértices."""
        if self.grafo:
            self.grafo._aristas = []
            self.grafo._adyacencia = {v.id: [] for v in self.grafo.vertices}
            self.pasos.append("Todas las conexiones fueron eliminadas.")
            self.paso_actual = len(self.pasos) - 1

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
