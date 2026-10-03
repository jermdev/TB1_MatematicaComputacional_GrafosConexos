import streamlit as st
from UI.components.controles import render_controles
from UI.components.grafo_canva import grafo_canva
from UI.components.progreso_pasos import progreso_pasos
from service.generador_grafo_service import (
    crear_grafo_ejemplo,
    crear_grafo_desde_texto,
    generar_grafo_aleatorio
)


def paso_atras():
    if st.session_state["paso_actual"] > 0:
        st.session_state["paso_actual"] -= 1


def paso_adelante():
    if st.session_state["paso_actual"] < len(st.session_state["pasos"]) - 1:
        st.session_state["paso_actual"] += 1


def render():
    st.set_page_config(layout="wide", page_title="Simulador de Grafos")

    # ---------- ESTADO INICIAL ----------
    if "pasos" not in st.session_state:
        st.session_state["pasos"] = [
            "Paso 1: Grafo inicializado. Listo para ejecutar algoritmos de conectividad.",
        ]
    if "paso_actual" not in st.session_state:
        st.session_state["paso_actual"] = 0 

    if "grafo" not in st.session_state:
        st.session_state["grafo"] = crear_grafo_ejemplo()

    if "vista" not in st.session_state:
        st.session_state["vista"] = "ambos"

    st.title("Simulador de Componentes Conexas de un Grafo")

    # ---------- LAYOUT PRINCIPAL: 3 COLUMNAS ----------
    # pesos relativos: pasos (angosto) | grafo (ancho) | controles (angosto)
    col_pasos, col_grafo, col_controles = st.columns([1, 3, 1.2])

    # ================= COLUMNA DERECHA: CONTROLES =================
    with col_controles:
        config = render_controles(paso_atras, paso_adelante)
        if config["generar"]:
            st.session_state["vista"] = config["vista"]
            try:
                if config["modo"] == "Manual":
                    nuevo_grafo = crear_grafo_desde_texto(
                        num_vertices=config["num_vertices"],
                        texto_conexiones=config["conexiones_texto"],
                        dirigido=config["dirigido"]
                    )
                else:
                    nuevo_grafo = generar_grafo_aleatorio(
                        num_vertices=config["num_vertices"],
                        dirigido=config["dirigido"]
                    )
                st.session_state["grafo"] = nuevo_grafo
                st.session_state["pasos"] = [
                    f"Grafo generado exitosamente ({len(nuevo_grafo.vertices)} vértices, {len(nuevo_grafo.aristas)} aristas, modo {config['modo']})."
                ]
                st.session_state["paso_actual"] = 0
                st.success("Grafo generado correctamente")
            except Exception as e:
                st.error(f"Error al generar el grafo: {e}")

    # ================= COLUMNA IZQUIERDA: PASO A PASO =================
    with col_pasos:
        progreso_pasos(st.session_state["pasos"], st.session_state["paso_actual"]) 

    # ================= COLUMNA CENTRAL: VISUALIZACION DEL GRAFO =================
    with col_grafo:
        vista_actual = config["vista"] if config else st.session_state.get("vista", "ambos")
        grafo_canva(st.session_state["grafo"], vista=vista_actual)