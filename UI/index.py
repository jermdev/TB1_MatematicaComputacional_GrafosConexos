import streamlit as st
from UI.components.controles import render_controles
from UI.components.grafo_canva import grafo_canva
from UI.components.progreso_pasos import progreso_pasos

st.set_page_config(layout="wide", page_title="Simulador de Grafos")

def paso_atras():
    if st.session_state["paso_actual"] > 0:
        st.session_state["paso_actual"] -= 1


def paso_adelante():
    if st.session_state["paso_actual"] < len(st.session_state["pasos"]) - 1:
        st.session_state["paso_actual"] += 1

def render():
    # ---------- ESTADO INICIAL ----------
    if "pasos" not in st.session_state:
        st.session_state["pasos"] = [
            "Paso 1: Visitando el vértice 0...",
            "Paso 2: Se encuentra la arista (0,1), se marca como visitada.",
            "Paso 3: ...",
        ]
    if "paso_actual" not in st.session_state:
        st.session_state["paso_actual"] = 0 

    st.title("Simulador de Componentes Conexas de un Grafo")

    # ---------- LAYOUT PRINCIPAL: 3 COLUMNAS ----------
    # pesos relativos: pasos (angosto) | grafo (ancho) | controles (angosto)
    col_pasos, col_grafo, col_controles = st.columns([1, 3, 1.2])

    # ================= COLUMNA IZQUIERDA: PASO A PASO =================
    with col_pasos:
        progreso_pasos(st.session_state["pasos"], st.session_state["paso_actual"]) 

    # ================= COLUMNA CENTRAL: VISUALIZACION DEL GRAFO =================
    with col_grafo:
        grafo_canva()

    # ================= COLUMNA DERECHA: CONTROLES =================
    with col_controles:
        render_controles(paso_atras, paso_adelante)