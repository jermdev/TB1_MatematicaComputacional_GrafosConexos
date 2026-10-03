import streamlit as st
from UI.components.controles import render_controles
from UI.components.grafo_canva import grafo_canva
from UI.components.progreso_pasos import progreso_pasos
from service.grafo_orquestador import GrafoOrquestador


def paso_atras():
    if "orquestador" in st.session_state:
        st.session_state["orquestador"].paso_atras()


def paso_adelante():
    if "orquestador" in st.session_state:
        st.session_state["orquestador"].paso_adelante()


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

        # Manejo de la acción: Generar grafo
        if datos_controles["generar"]:
            orquestador.generar_grafo(
                num_vertices=datos_controles["num_vertices"],
                modo=datos_controles["modo"],
                algoritmo=datos_controles["algoritmo"],
                probabilidad=datos_controles.get("densidad", 0.35),
            )
            st.rerun()

        # Manejo de la acción: Conectar vértices manualmente
        if datos_controles.get("conectar_manual"):
            origen = datos_controles["origen_manual"]
            destino = datos_controles["destino_manual"]
            exito, mensaje = orquestador.agregar_conexion_manual(origen, destino)
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
        progreso_pasos(orquestador.pasos, orquestador.paso_actual)

    # ================= COLUMNA CENTRAL: VISUALIZACION DEL GRAFO O MATRIZ =================
    with col_grafo:
        # Cabecera con selector y botón para alternar vistas
        c_titulo, c_toggle = st.columns([2, 1.4])
        with c_titulo:
            modo_badge = "🎲 Automático" if orquestador.modo == "Automático" else "✋ Manual"
            st.subheader(f"Visualización ({modo_badge})")

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
        )