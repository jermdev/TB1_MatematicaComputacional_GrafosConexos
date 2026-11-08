import streamlit as st
from UI.components.controles import render_controles
from UI.components.grafo_canva import grafo_canva
from UI.components.progreso_pasos import progreso_pasos
from service.grafo_orquestador import GrafoOrquestador

def main():
    # Inicializamos el orquestador y lo guardamos en la memoria de la sesión
    if 'orquestador' not in st.session_state:
        st.session_state.orquestador = GrafoOrquestador()

    # Le pasamos el orquestador a la función render de la interfaz
    render()

def paso_atras():
    if "orquestador" in st.session_state:
        st.session_state["orquestador"].paso_atras()
        st.rerun()

def paso_adelante():
    if "orquestador" in st.session_state:
        st.session_state["orquestador"].paso_adelante()
        st.rerun()

def render():
    st.set_page_config(
        layout="wide",
        page_title="Simulador de Grafos Conexos",
        page_icon="🕸️",
    )

    # ---------- ESTADO INICIAL DEL ORQUESTADOR ----------
    if "orquestador" not in st.session_state:
        st.session_state["orquestador"] = GrafoOrquestador()

    orquestador: GrafoOrquestador = st.session_state["orquestador"]

    st.title("🕸️ Simulador de Componentes Conexas de un Grafo")

    # Mensaje de estado reciente (si existe)
    if orquestador.ultimo_mensaje:
        st.toast(orquestador.ultimo_mensaje)

    # ---------- LAYOUT PRINCIPAL: 3 COLUMNAS ----------
    # pasos (angosto) | visualización del grafo/matriz (ancho) | controles (angosto)
    col_pasos, col_grafo, col_controles = st.columns([1, 2.8, 1.2])

    # ================= COLUMNA DERECHA: CONTROLES =================
    # Renderizamos y capturamos los datos antes para procesar eventos en este ciclo
    with col_controles:
        datos_controles = render_controles(
            orquestador=orquestador,
            paso_atras=paso_atras,
            paso_adelante=paso_adelante,
        )

        # Sincronización del modo si el usuario lo cambió en los controles
        if datos_controles["modo"] != orquestador.modo:
            orquestador.cambiar_modo(datos_controles["modo"])

        # Sincronización del tipo de grafo (Dirigido / No dirigido)
        if datos_controles["dirigido"] != orquestador.es_dirigido():
            orquestador.cambiar_dirigido(datos_controles["dirigido"])
            st.rerun()

        # Sincronización del criterio de conectividad en grafos dirigidos (Fuerte / Débil)
        if datos_controles["fuertemente"] != getattr(orquestador, "fuertemente", True):
            orquestador.cambiar_tipo_conectividad(datos_controles["fuertemente"])
            st.rerun()

        # Sincronización de algoritmo si el usuario lo cambió en los controles
        if datos_controles["algoritmo"] != orquestador.algoritmo_seleccionado:
            orquestador.algoritmo_seleccionado = datos_controles["algoritmo"]
            orquestador.actualizar_algoritmo(paso_inicial=0)
            st.rerun()

        # Manejo de la acción: Generar grafo
        if datos_controles["generar"]:
            orquestador.generar_grafo(
                num_vertices=datos_controles["num_vertices"],
                modo=datos_controles["modo"],
                algoritmo=datos_controles["algoritmo"],
                probabilidad=datos_controles.get("densidad", 0.35),
                dirigido=datos_controles["dirigido"],
            )
            st.rerun()

        # Manejo de la acción: Conectar vértices manualmente
        if datos_controles.get("conectar_manual"):
            origen = datos_controles["origen_manual"]
            destino = datos_controles["destino_manual"]
            exito, mensaje = orquestador.agregar_conexion_manual(
                origen,
                destino,
                dirigida=datos_controles["dirigido"],
            )
            if not exito:
                st.warning(mensaje)
            else:
                st.rerun()

        # Manejo de la acción: Cancelar conexión manual
        if datos_controles.get("cancelar_manual"):
            origen = datos_controles.get("origen_manual")
            destino = datos_controles.get("destino_manual")
            if origen and destino and orquestador.existe_conexion(origen, destino):
                exito, mensaje = orquestador.eliminar_conexion_manual(origen, destino)
            else:
                exito, mensaje = orquestador.cancelar_ultima_conexion()
            if not exito:
                st.warning(mensaje)
            else:
                st.rerun()

        # Manejo de la acción: Limpiar aristas manuales
        if datos_controles.get("limpiar_manual"):
            orquestador.limpiar_conexiones()
            st.rerun()

    # ================= COLUMNA IZQUIERDA: PASO A PASO =================
    with col_pasos:
        progreso_pasos(
            pasos=orquestador.pasos,
            paso_actual=orquestador.paso_actual,
            componentes_conexas=getattr(orquestador, "componentes_conexas", []),
            obtener_etiqueta=orquestador.obtener_etiqueta_vertice,
            dirigido=orquestador.es_dirigido(),
            fuertemente=getattr(orquestador, "fuertemente", True),
            componentes_fuertemente_conexas=orquestador.obtener_componentes_fuertemente_conexas(),
            componentes_debilmente_conexas=orquestador.obtener_componentes_debilmente_conexas(),
        )

    # ================= COLUMNA CENTRAL: VISUALIZACION DEL GRAFO O MATRIZ =================
    with col_grafo:
        # Cabecera con selector y botón para alternar vistas
        c_titulo, c_toggle = st.columns([2, 1.4])
        with c_titulo:
            modo_badge = "🎲 Automático" if orquestador.modo == "Automático" else "✋ Manual"
            dir_badge = "↗️ Dirigido" if orquestador.es_dirigido() else "↔️ No dirigido"
            st.subheader(f"Visualización ({modo_badge} · {dir_badge})")

        with c_toggle:
            texto_btn = (
                "🔢 Cambiar a Matriz"
                if orquestador.vista_actual == "grafo"
                else "🕸️ Cambiar a Grafo"
            )
            if st.button(
                f"🔄 {texto_btn}",
                use_container_width=True,
                key="btn_toggle_vista",
            ):
                orquestador.alternar_vista()
                st.rerun()

        grafo_canva(
            grafo=orquestador.obtener_grafo(),
            vista=orquestador.vista_actual,
            modo_manual=(orquestador.modo == "Manual"),
            paso_actual=orquestador.paso_actual,
            pasos_algoritmo=getattr(orquestador, "pasos_algoritmo", []),
            componentes_conexas=getattr(orquestador, "componentes_conexas", []),
            grafo_id=getattr(orquestador, "grafo_id", "default"),
            fuertemente=getattr(orquestador, "fuertemente", True),
	    orquestador=orquestador
        )